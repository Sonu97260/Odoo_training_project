/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { registry } from "@web/core/registry";
import { ListRenderer } from "@web/views/list/list_renderer";

patch(ListRenderer.prototype, {
    setup() {
        this._super(...arguments);
        $(document).on('click', '.o_field_many2many .o_attachment', (ev) => {
            ev.stopPropagation();
            const attId = $(ev.currentTarget).data('id');
            if (attId) {
            
                this.env.services.action.doAction('ir.actions.act_window', {
                    type: 'ir.actions.act_window',
                    res_model: 'ir.attachment',
                    views: [[false, 'form']],
                    res_id: attId,
                    target: 'new',
                    context: { 'preview_document': true },
                });
            }
        });
    },
});