import { Deserializable } from "./deserializable.model";

export class AuthResponse implements Deserializable {
    access_token: string;

    deserialize(input: any): this {
        if (input) {
            Object.assign(this, input)
        }
        return this
    }
}
