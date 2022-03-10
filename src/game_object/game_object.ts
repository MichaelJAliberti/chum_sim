import {Point} from "../../src/movement/point";

export class GameObject {
    location: Point;

    constructor(x: number = 0, y: number = 0) {
        this.location = new Point(x, y)
    }
}