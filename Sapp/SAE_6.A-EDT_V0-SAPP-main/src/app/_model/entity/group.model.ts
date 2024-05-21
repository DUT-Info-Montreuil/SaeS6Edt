import { Deserializable } from "../fonctional/deserializable.model"

export class Group implements Deserializable {
    id: number;
    name: string;
    id_group_parent: number;
    children: Group[];

    deserialize(input: any): this {
        if (input) {
            Object.assign(this, input)
        }
        return this
    }
}
