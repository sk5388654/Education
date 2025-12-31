frappe.ui.form.ControlData = class ControlData extends frappe.ui.form.ControlData {
    make_input() {
        super.make_input();

        // activate only when options == "awesome_button"
        if (this.df.options === "awesome_button") {
            const btn = $('<button class="btn btn-xs btn-secondary" style="margin-left: 7px;">Click</button>');
            btn.on('click', () => {
                frappe.msgprint("You clicked the awesome button!");
            });
            $(this.input).after(btn);
        }
    }
};
