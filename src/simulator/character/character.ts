import { GameObject } from '../game_object/game_object'

export class Character extends GameObject {
    // attributes
    bod: number
    agi: number
    rea: number
    str: number
    wil: number
    log: number
    int: number
    cha: number

    // special attributes
    edg: number
    ess: number
    ini: number
    mag: number
    res: number
}
