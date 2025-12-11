/** @odoo-module */
import { Many2ManyBinaryField } from "@web/views/fields/many2many_binary/many2many_binary_field";
import { patch } from "@web/core/utils/patch";
import { useFileViewer } from "@web/core/file_viewer/file_viewer_hook";

patch(Many2ManyBinaryField.prototype, {
    setup() {
        super.setup(...arguments);
        this.fileViewer = useFileViewer();
    },

    onClickPreview(file, files) {
        if (!file || !files) {
            console.warn("File or files undefined, cannot preview");
            return;
        }

        const attachments = files.map(f => ({
            id: f.id,
            name: f.name,
            filename: f.name,
            mimetype: f.mimetype,
            type: "binary",
        }));

        const attachment = attachments.find(a => a.id === file.id);

        if (attachment) {
            this.fileViewer.open(attachment, attachments);
        }
    },
});
