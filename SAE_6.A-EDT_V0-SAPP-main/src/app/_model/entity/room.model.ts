import { Deserializable } from "../fonctional/deserializable.model"

export class Room implements Deserializable {
    nom: string;
    ordi: number;
    tableauNumerique: number
    videoProjecteur: number;
    
    deserialize(input: any): this {
        if (input) {
            Object.assign(this, input)
        }
        return this
    }
}
