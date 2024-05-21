import { Staff } from "./staff.model";

export class Teacher {
    id: number;
    staff: Staff;
    activated: boolean

    constructor(id: number, name: string, lastname: string, username: string, password: string, activated: boolean){
        this.activated = activated;
        this.id = id;
        this.staff = new Staff(name, lastname, username, password);
    }
}
