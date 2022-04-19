import { Point } from '../../src/movement/point'

export class GameObject {
    location: Point

    constructor(x = 0, y = 0) {
        this.location = new Point(x, y)
    }
}
