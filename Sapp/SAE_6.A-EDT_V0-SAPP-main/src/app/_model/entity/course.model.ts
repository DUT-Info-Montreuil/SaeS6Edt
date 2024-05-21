// Importing the Deserializable interface for data deserialization
import { Deserializable } from "../fonctional/deserializable.model"

export class Course implements Deserializable {
    id: number;
    start_time: Date;
    end_time: Date;
    id_enseignant?: number;
    initial_ressource: string;
    id_group: number;
    name_salle?: string;
    appelEffectue: boolean;
    is_published: boolean;
    evaluation: boolean;

    // Deserialization method to convert received data into an instance of the class
    deserialize(input: any): this {
        if (input) {
            Object.assign(this, input)
        }
        return this
    }
}
