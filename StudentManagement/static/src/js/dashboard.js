/** @odoo-module **/
import { Component, useState, onMounted } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";

export class StudentDashboard extends Component {
    static template = "owl.StudentDashboard";
    
    setup() {
        this.orm = useService("orm");
        this.state = useState({ total: 0 });
     
     
        onMounted(async () => {
                // const chartData = await this.orm.call("rest.student", "get_marks_chart_data", []);
                // this.state.chartData = chartData;

                const data = await this.orm.call("rest.student", "get_dashboard_data", []);
                this.state.total = data.total || 0;

                const data_teacher = await this.orm.call("teacher.teacher", "get_teacher_count", []);
                this.state.total_teachers = data_teacher.total_teachers || 0;

                const data_subject = await this.orm.call("school.subject", "get_subject_count", []);
                this.state.total_subjects = data_subject.total_subjects || 0;
        });
     }
    //    async openStudents() {

    //         const actionData = await this.orm.call(
    //             "ir.actions.actions",
    //             "get_dashboard_data",
    //             ["StudentManagement.get_dashboard_data"]
    //         );

    //         if (actionData && actionData.action) {
    //             this.action.doAction(actionData.action);
    //         }
    //     }
    }
registry.category("actions").add("StudentDashboard", StudentDashboard);
