import { Staff } from "./staff.model";

// The EdtManager class represents the front-end entity corresponding to an timetable manager.
export class EdtManager {
    id: number;
    staff: Staff;
    name: string;
    lastname: string;
    username: string;
    password?: string

    // Constructor to initialize the EdtManager instance with basic details
    constructor(id: number, name: string, lastname: string, username: string, password: string){
        this.id = id;
        this.name = name;
        this.lastname = lastname;
        this.username = username;
        this.password = password;
        this.staff = new Staff(name, lastname, username, password);
    }
}
