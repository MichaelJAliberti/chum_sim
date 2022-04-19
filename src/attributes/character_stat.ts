import { BaseStat } from './base_stat'

export class CharacterStat extends BaseStat {
    name: string
    value: number
    _cost_mult: number

    constructor(name: string, value: number, mult: number) {
        super(name, value)
        this._cost_mult = mult
    }

    check_cost(new_value = this.value + 1) {
        let cost = 0
        for (let i = new_value; i > this.value; i--) cost += i * this._cost_mult
        return cost
    }
}
