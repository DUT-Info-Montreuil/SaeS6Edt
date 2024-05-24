import { User } from "./user.model";

export class Staff {
    id: number;
    initial: string;
    user : User;
    
    constructor(name: string, lastname: string, username: string, password: string){
        this.user = new User(name, lastname, username, password);
    }
}
