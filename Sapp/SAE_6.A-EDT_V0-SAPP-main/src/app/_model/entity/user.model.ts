
export class User {
    id: number;
    username: string;
    password?: string
    role: string;
    name: string;
    lastname: string;

    constructor(name: string, lastname: string, username: string, password: string){
        this.name = name;
        this.lastname = lastname;
        this.username = username;
        this.password = password;
    }
}
