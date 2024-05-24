import { User } from "./user.model";

export class Student{
    id: number;
    INE : number;
    user : User;

    constructor(id: number, INE: number, name: string, lastname: string, username: string, password: string){
        this.id = id;
        this.INE = INE;
        this.user = new User(name, lastname, username, password);
    }
}
