/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onMounted } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class JobDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({ total: 0 });

        onMounted(async () => {
            try {
                const data = await this.orm.call("job.position", "get_dashboard_data", []);
                this.state.total = data.total || 0; 
            } catch (error) {
                console.error("Error loading dashboard:", error);
            }
        });
    }
}
JobDashboard.template = "owl.job_dashboard_tag";
registry.category("actions").add("JobDashboard",job_dashboard_tag);
// OdooDynamicDashboard.template = "owl.OdooDynamicDashboard";
// registry.category("actions").add("OdooDynamicDashboard", OdooDynamicDashboard);

