"""txt2img top-level tab UI (M22)."""
from __future__ import annotations

from modules.ui_tab_build_result import TabBuildResult


def create_txt2img_tab():
    from contextlib import ExitStack

    import gradio as gr
    import modules.infotext_utils as parameters_copypaste
    import modules.sd_models
    import modules.shared as shared
    import modules.txt2img
    import modules.ui as ui
    from modules import progress, scripts, sd_samplers, sd_schedulers, ui_extra_networks, ui_toprow
    from modules.call_queue import wrap_gradio_gpu_call, wrap_queued_call
    from modules.infotext_utils import PasteField
    from modules.shared import opts
    from modules.ui_common import create_refresh_button
    from modules.ui_components import FormGroup, FormHTML, FormRow, InputAccordion, ResizeHandleRow, ToolButton

    with gr.Blocks(analytics_enabled=False) as txt2img_interface:
        toprow = ui_toprow.Toprow(is_img2img=False, is_compact=shared.opts.compact_prompt_box)

        dummy_component = gr.Label(visible=False)

        extra_tabs = gr.Tabs(elem_id="txt2img_extra_tabs", elem_classes=["extra-networks"])
        extra_tabs.__enter__()

        with gr.Tab("Generation", id="txt2img_generation") as txt2img_generation_tab, ResizeHandleRow(equal_height=False):
            with ExitStack() as stack:
                if shared.opts.txt2img_settings_accordion:
                    stack.enter_context(gr.Accordion("Open for Settings", open=False))
                stack.enter_context(gr.Column(variant='compact', elem_id="txt2img_settings"))

                scripts.scripts_txt2img.prepare_ui()

                for category in ui.ordered_ui_categories():
                    if category == "prompt":
                        toprow.create_inline_toprow_prompts()

                    elif category == "dimensions":
                        with FormRow():
                            with gr.Column(elem_id="txt2img_column_size", scale=4):
                                width = gr.Slider(minimum=64, maximum=2048, step=8, label="Width", value=512, elem_id="txt2img_width")
                                height = gr.Slider(minimum=64, maximum=2048, step=8, label="Height", value=512, elem_id="txt2img_height")

                            with gr.Column(elem_id="txt2img_dimensions_row", scale=1, elem_classes="dimensions-tools"):
                                res_switch_btn = ToolButton(value=ui.switch_values_symbol, elem_id="txt2img_res_switch_btn", tooltip="Switch width/height")

                            if opts.dimensions_and_batch_together:
                                with gr.Column(elem_id="txt2img_column_batch"):
                                    batch_count = gr.Slider(minimum=1, step=1, label='Batch count', value=1, elem_id="txt2img_batch_count")
                                    batch_size = gr.Slider(minimum=1, maximum=8, step=1, label='Batch size', value=1, elem_id="txt2img_batch_size")

                    elif category == "cfg":
                        with gr.Row():
                            cfg_scale = gr.Slider(minimum=1.0, maximum=30.0, step=0.5, label='CFG Scale', value=7.0, elem_id="txt2img_cfg_scale")

                    elif category == "checkboxes":
                        with FormRow(elem_classes="checkboxes-row", variant="compact"):
                            pass

                    elif category == "accordions":
                        with gr.Row(elem_id="txt2img_accordions", elem_classes="accordions"):
                            with InputAccordion(False, label="Hires. fix", elem_id="txt2img_hr") as enable_hr:
                                with enable_hr.extra():
                                    hr_final_resolution = FormHTML(value="", elem_id="txtimg_hr_finalres", label="Upscaled resolution", interactive=False, min_width=0)

                                with FormRow(elem_id="txt2img_hires_fix_row1", variant="compact"):
                                    hr_upscaler = gr.Dropdown(label="Upscaler", elem_id="txt2img_hr_upscaler", choices=[*shared.latent_upscale_modes, *[x.name for x in shared.sd_upscalers]], value=shared.latent_upscale_default_mode)
                                    hr_second_pass_steps = gr.Slider(minimum=0, maximum=150, step=1, label='Hires steps', value=0, elem_id="txt2img_hires_steps")
                                    denoising_strength = gr.Slider(minimum=0.0, maximum=1.0, step=0.01, label='Denoising strength', value=0.7, elem_id="txt2img_denoising_strength")

                                with FormRow(elem_id="txt2img_hires_fix_row2", variant="compact"):
                                    hr_scale = gr.Slider(minimum=1.0, maximum=4.0, step=0.05, label="Upscale by", value=2.0, elem_id="txt2img_hr_scale")
                                    hr_resize_x = gr.Slider(minimum=0, maximum=2048, step=8, label="Resize width to", value=0, elem_id="txt2img_hr_resize_x")
                                    hr_resize_y = gr.Slider(minimum=0, maximum=2048, step=8, label="Resize height to", value=0, elem_id="txt2img_hr_resize_y")

                                with FormRow(elem_id="txt2img_hires_fix_row3", variant="compact", visible=opts.hires_fix_show_sampler) as hr_sampler_container:

                                    hr_checkpoint_name = gr.Dropdown(label='Checkpoint', elem_id="hr_checkpoint", choices=["Use same checkpoint"] + modules.sd_models.checkpoint_tiles(use_short=True), value="Use same checkpoint")
                                    create_refresh_button(hr_checkpoint_name, modules.sd_models.list_models, lambda: {"choices": ["Use same checkpoint"] + modules.sd_models.checkpoint_tiles(use_short=True)}, "hr_checkpoint_refresh")

                                    hr_sampler_name = gr.Dropdown(label='Hires sampling method', elem_id="hr_sampler", choices=["Use same sampler"] + sd_samplers.visible_sampler_names(), value="Use same sampler")
                                    hr_scheduler = gr.Dropdown(label='Hires schedule type', elem_id="hr_scheduler", choices=["Use same scheduler"] + [x.label for x in sd_schedulers.schedulers], value="Use same scheduler")

                                with FormRow(elem_id="txt2img_hires_fix_row4", variant="compact", visible=opts.hires_fix_show_prompts) as hr_prompts_container:
                                    with gr.Column(scale=80):
                                        with gr.Row():
                                            hr_prompt = gr.Textbox(label="Hires prompt", elem_id="hires_prompt", show_label=False, lines=3, placeholder="Prompt for hires fix pass.\nLeave empty to use the same prompt as in first pass.", elem_classes=["prompt"])
                                    with gr.Column(scale=80):
                                        with gr.Row():
                                            hr_negative_prompt = gr.Textbox(label="Hires negative prompt", elem_id="hires_neg_prompt", show_label=False, lines=3, placeholder="Negative prompt for hires fix pass.\nLeave empty to use the same negative prompt as in first pass.", elem_classes=["prompt"])

                            scripts.scripts_txt2img.setup_ui_for_section(category)

                    elif category == "batch":
                        if not opts.dimensions_and_batch_together:
                            with FormRow(elem_id="txt2img_column_batch"):
                                batch_count = gr.Slider(minimum=1, step=1, label='Batch count', value=1, elem_id="txt2img_batch_count")
                                batch_size = gr.Slider(minimum=1, maximum=8, step=1, label='Batch size', value=1, elem_id="txt2img_batch_size")

                    elif category == "override_settings":
                        with FormRow(elem_id="txt2img_override_settings_row") as row:
                            override_settings = ui.create_override_settings_dropdown('txt2img', row)

                    elif category == "scripts":
                        with FormGroup(elem_id="txt2img_script_container"):
                            custom_inputs = scripts.scripts_txt2img.setup_ui()

                    if category not in {"accordions"}:
                        scripts.scripts_txt2img.setup_ui_for_section(category)

            hr_resolution_preview_inputs = [enable_hr, width, height, hr_scale, hr_resize_x, hr_resize_y]

            for component in hr_resolution_preview_inputs:
                event = component.release if isinstance(component, gr.Slider) else component.change

                event(
                    fn=ui.calc_resolution_hires,
                    inputs=hr_resolution_preview_inputs,
                    outputs=[hr_final_resolution],
                    show_progress=False,
                )
                event(
                    None,
                    _js="onCalcResolutionHires",
                    inputs=hr_resolution_preview_inputs,
                    outputs=[],
                    show_progress=False,
                )

            output_panel = ui.create_output_panel("txt2img", opts.outdir_txt2img_samples, toprow)

            txt2img_inputs = [
                dummy_component,
                toprow.prompt,
                toprow.negative_prompt,
                toprow.ui_styles.dropdown,
                batch_count,
                batch_size,
                cfg_scale,
                height,
                width,
                enable_hr,
                denoising_strength,
                hr_scale,
                hr_upscaler,
                hr_second_pass_steps,
                hr_resize_x,
                hr_resize_y,
                hr_checkpoint_name,
                hr_sampler_name,
                hr_scheduler,
                hr_prompt,
                hr_negative_prompt,
                override_settings,
            ] + custom_inputs

            txt2img_outputs = [
                output_panel.gallery,
                output_panel.generation_info,
                output_panel.infotext,
                output_panel.html_log,
            ]

            txt2img_args = dict(
                fn=wrap_gradio_gpu_call(modules.txt2img.txt2img, extra_outputs=[None, '', '']),
                _js="submit",
                inputs=txt2img_inputs,
                outputs=txt2img_outputs,
                show_progress=False,
            )

            toprow.prompt.submit(**txt2img_args)
            toprow.submit.click(**txt2img_args)

            output_panel.button_upscale.click(
                fn=wrap_gradio_gpu_call(modules.txt2img.txt2img_upscale, extra_outputs=[None, '', '']),
                _js="submit_txt2img_upscale",
                inputs=txt2img_inputs[0:1] + [output_panel.gallery, dummy_component, output_panel.generation_info] + txt2img_inputs[1:],
                outputs=txt2img_outputs,
                show_progress=False,
            )

            res_switch_btn.click(fn=None, _js="function(){switchWidthHeight('txt2img')}", inputs=None, outputs=None, show_progress=False)

            toprow.restore_progress_button.click(
                fn=progress.restore_progress,
                _js="restoreProgressTxt2img",
                inputs=[dummy_component],
                outputs=[
                    output_panel.gallery,
                    output_panel.generation_info,
                    output_panel.infotext,
                    output_panel.html_log,
                ],
                show_progress=False,
            )

            txt2img_paste_fields = [
                PasteField(toprow.prompt, "Prompt", api="prompt"),
                PasteField(toprow.negative_prompt, "Negative prompt", api="negative_prompt"),
                PasteField(cfg_scale, "CFG scale", api="cfg_scale"),
                PasteField(width, "Size-1", api="width"),
                PasteField(height, "Size-2", api="height"),
                PasteField(batch_size, "Batch size", api="batch_size"),
                PasteField(toprow.ui_styles.dropdown, lambda d: d["Styles array"] if isinstance(d.get("Styles array"), list) else gr.update(), api="styles"),
                PasteField(denoising_strength, "Denoising strength", api="denoising_strength"),
                PasteField(enable_hr, lambda d: "Denoising strength" in d and ("Hires upscale" in d or "Hires upscaler" in d or "Hires resize-1" in d), api="enable_hr"),
                PasteField(hr_scale, "Hires upscale", api="hr_scale"),
                PasteField(hr_upscaler, "Hires upscaler", api="hr_upscaler"),
                PasteField(hr_second_pass_steps, "Hires steps", api="hr_second_pass_steps"),
                PasteField(hr_resize_x, "Hires resize-1", api="hr_resize_x"),
                PasteField(hr_resize_y, "Hires resize-2", api="hr_resize_y"),
                PasteField(hr_checkpoint_name, "Hires checkpoint", api="hr_checkpoint_name"),
                PasteField(hr_sampler_name, sd_samplers.get_hr_sampler_from_infotext, api="hr_sampler_name"),
                PasteField(hr_scheduler, sd_samplers.get_hr_scheduler_from_infotext, api="hr_scheduler"),
                PasteField(hr_sampler_container, lambda d: gr.update(visible=True) if d.get("Hires sampler", "Use same sampler") != "Use same sampler" or d.get("Hires checkpoint", "Use same checkpoint") != "Use same checkpoint" or d.get("Hires schedule type", "Use same scheduler") != "Use same scheduler" else gr.update()),
                PasteField(hr_prompt, "Hires prompt", api="hr_prompt"),
                PasteField(hr_negative_prompt, "Hires negative prompt", api="hr_negative_prompt"),
                PasteField(hr_prompts_container, lambda d: gr.update(visible=True) if d.get("Hires prompt", "") != "" or d.get("Hires negative prompt", "") != "" else gr.update()),
                *scripts.scripts_txt2img.infotext_fields
            ]
            parameters_copypaste.add_paste_fields("txt2img", None, txt2img_paste_fields, override_settings)
            parameters_copypaste.register_paste_params_button(parameters_copypaste.ParamBinding(
                paste_button=toprow.paste, tabname="txt2img", source_text_component=toprow.prompt, source_image_component=None,
            ))

            steps = scripts.scripts_txt2img.script('Sampler').steps

            txt2img_preview_params = [
                toprow.prompt,
                toprow.negative_prompt,
                steps,
                scripts.scripts_txt2img.script('Sampler').sampler_name,
                cfg_scale,
                scripts.scripts_txt2img.script('Seed').seed,
                width,
                height,
            ]

            toprow.ui_styles.dropdown.change(fn=wrap_queued_call(ui.update_token_counter), inputs=[toprow.prompt, steps, toprow.ui_styles.dropdown], outputs=[toprow.token_counter])
            toprow.ui_styles.dropdown.change(fn=wrap_queued_call(ui.update_negative_prompt_token_counter), inputs=[toprow.negative_prompt, steps, toprow.ui_styles.dropdown], outputs=[toprow.negative_token_counter])
            toprow.token_button.click(fn=wrap_queued_call(ui.update_token_counter), inputs=[toprow.prompt, steps, toprow.ui_styles.dropdown], outputs=[toprow.token_counter])
            toprow.negative_token_button.click(fn=wrap_queued_call(ui.update_negative_prompt_token_counter), inputs=[toprow.negative_prompt, steps, toprow.ui_styles.dropdown], outputs=[toprow.negative_token_counter])

        extra_networks_ui = ui_extra_networks.create_ui(txt2img_interface, [txt2img_generation_tab], 'txt2img')
        ui_extra_networks.setup_ui(extra_networks_ui, output_panel.gallery)

        extra_tabs.__exit__()
    return TabBuildResult(
        txt2img_interface,
        "txt2img",
        "txt2img",
        dummy_component,
        txt2img_preview_params=txt2img_preview_params,
    )
