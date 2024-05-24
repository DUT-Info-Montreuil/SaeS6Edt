import { Deserializable } from "../fonctional/deserializable.model"

export class WeekComment implements Deserializable {
    id: number;
    year: string;
    content: string;
    week_number: number;
    id_promo: number;

    deserialize(input: any): this {
        if (input) {
            Object.assign(this, input)
        }
        return this
    }
}
