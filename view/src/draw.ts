import { Partition, TileMap, TileEdge } from './types'

function polygon(ctx, points: number[][], scale:number=1) {
    ctx.beginPath()
    ctx.moveTo(scale*points[0][0], scale*points[0][1])
    for (let i = 1; i < points.length; i++) {
        ctx.lineTo(scale*points[i][0], scale*points[i][1])
    }
    ctx.lineTo(scale*points[0][0], scale*points[0][1])
    ctx.closePath()
}

export function draw_partition(
    canvas: HTMLCanvasElement,
    ctx: any,
    map: TileMap,
    partition: Partition,
    colors: string[]
) {
    const [ xmin, ymin, xmax, ymax ] = map.bbox
    partition.forEach((district_idx:number, tile_idx:number) => {
        ctx.lineWidth = 1
        ctx.fillStyle = colors[district_idx]
        ctx.strokeStyle = 'lightgray'//colors[district_idx]

        const scale = Math.min(canvas.width/(xmax-xmin), canvas.height/(ymax-ymin))

        polygon(ctx, map.vertices[tile_idx].map(([x, y]) => {
            return [(x-xmin) * scale, canvas.height - (y-ymin) * scale]
        }))

        ctx.fill()
        ctx.stroke()

        ctx.strokeStyle = 'black'
        ctx.lineWidth = 3
        // for (const edge of map.tile_edges[tile_idx]) {
        //     const adjacent_district = partition[edge.adjacent_cell]
        //     if (edge.adjacent_cell < 0 || adjacent_district != district_idx) {
        //         const [v1, v2] = edge.vertices

        //         const [x1, y1] = map.tile_vertices[tile_idx][v1]
        //         const [x2, y2] = map.tile_vertices[tile_idx][v2]

        //         ctx.beginPath()
        //         ctx.moveTo(x1*scale, y1*scale)
        //         ctx.lineTo(x2*scale, y2*scale)
        //         ctx.stroke()
        //     }
        // }

    })
}