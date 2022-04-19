import { Point } from './src/movement/point'
import { Attribute } from './src/attributes/attribute'

const pt = new Point(1, 2)
console.log(`(${pt.x}, ${pt.y})`)

const str = new Attribute('Strength')
console.log(str.check_cost())
