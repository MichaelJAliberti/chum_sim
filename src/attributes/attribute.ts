import { CharacterStat } from './character_stat'

export class Attribute extends CharacterStat {
    abbrev: string

    constructor(name: string, value = 3) {
        super(name, value, 5)
        this.abbrev = name.substring(0, 3)
    }
}
