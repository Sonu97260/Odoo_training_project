/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onMounted } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class StudentDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({ total: 0 });

        onMounted(async () => {
            try {
                const data = await this.orm.call("rest.student", "get_dashboard_data", []);
                this.state.total = data.total || 0;
            } catch (error) {
                console.error("Error loading dashboard:", error);
            }
        });
    }
}

StudentDashboard.template = "owl.StudentDashboard";
registry.category("actions").add("StudentDashboard",StudentDashboard);




