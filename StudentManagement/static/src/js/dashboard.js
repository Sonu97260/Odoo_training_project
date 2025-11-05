/** @odoo-module **/
import { Component, useState, onMounted } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";

export class StudentDashboard extends Component {
    static template = "owl.StudentDashboard";
    
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            students:[],
            student_cancel:[],
            searchView: "",
            total: 0,
            total_teachers: 0,
            total_subject: 0, 
        });
        onMounted(async () => {

                const student_data= await this.orm.searchRead('rest.student',[["state","=","confirmed"]],
                    ["name","age","email","gender","state"]
                );
                console.log("Fetched students://///////", student_data);

                this.state.students = student_data.map((stu) => ({
                id: stu.id,
                name: stu.name,
                age: stu.age,
                email: stu.email ,
                gender: stu.gender,
                state: stu.state,
            }));
            this.state.total=student_data.length;

            const cancel_student=await this.orm.searchRead('rest.student',[["state","=","cancelled"]],
                ["name","age","email","gender","state"],
            );     
            console.log("cancel students://///////", cancel_student);

            this.state.student_cancel=cancel_student.map((stud) =>({
                id: stud.id,
                name: stud.name,
                age: stud.age,
                email: stud.email ,
                gender: stud.gender,
                state: stud.state,  
            }));
            this.state.total=student_data.length;

                const data = await this.orm.call("rest.student", "get_dashboard_data", []);
                this.state.total = data.total || 0;

                const data_teacher = await this.orm.call("teacher.teacher", "get_teacher_count", []);
                this.state.total_teachers = data_teacher.total_teachers || 0;

                const data_subject = await this.orm.call("school.subject", "get_subject_count", []);
                this.state.total_subjects = data_subject.total_subjects || 0;
        });
     }

    }
registry.category("actions").add("StudentDashboard", StudentDashboard);
