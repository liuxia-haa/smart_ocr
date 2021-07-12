
function BoxStr2ArrayInt(str) {
    var box = str.split(',');
    for (let i = 0; i < box.length; i++) {
        box[i] = parseInt(box[i])
    }
    return box;
}
//原始图片的坐标信息，是4个整数以逗号 分隔的方式组成的字符串，4个整数从左到右分别代表文本块的左 上⻆ 横坐标、左上⻆纵坐标、宽度、高度;
function getOverlapbox(box1, box2) {
    box1 = BoxStr2ArrayInt(box1);
    box2 = BoxStr2ArrayInt(box2);
        //两个矩形在水平方向下方或上方，完全不重叠
        if (box1[1] > box2[1]+box2[3] || box1[1]+box1[3] < box2[1]) {
            return 0;
        }
        //两个矩形在垂直方向左侧或右侧，完全不重叠
        if (box1[0] > box2[0]+box2[2] || box1[0]+box1[2] < box2[0]) {
            return 0;
        }
        //重叠区域长乘宽
        var side1 = 0;
        var side2 = 0;
        if (box1[1]>box2[1] && box1[1] < box2[1]+box2[3]) {
            side1 = box2[1]+box2[3] - box1[1];
        } else if(box2[1]>box1[1] && box2[1]<box1[1]+box1[3]) {
            side1 = box1[1]+box1[3] - box2[1];
        }
        if (box1[0] > box2[0] && box1[0]<box2[0]+box2[2]) {
            side2 = box2[0]+box2[2] - box1[0];
        } else if (box2[0] > box1[0] && box2[0]<box1[0]+box1[2]){
            side2 = box1[0]+box1[2] - box2[2];
        }
        return side1 * side2 
}
/*
function getOverlapArea(str1, str2) {

    var box1 = BoxStr2ArrayInt(str1);
    var box2 = BoxStr2ArrayInt(str2);
    //两个矩形在水平方向下方或上方，完全不重叠
    if (box1[1] > box2[7] || box1[7] < box2[1]) {
        return 0;
    }
    //两个矩形在垂直方向左侧或右侧，完全不重叠
    if (box1[0] > box2[2] || box1[2] < box2[0]) {
        return 0;
    }
    //重叠区域长乘宽
    var side1 = 0;
    var side2 = 0;
    if (box1[1] < box2[7]) {
        side1 = box2[7] - box1[1];
    } else {
        side1 = box1[1] - box2[7];
    }
    if (box1[0] < box2[2]) {
        side2 = box2[2] - box1[0];
    } else {
        side2 = box1[0] - box2[2];
    }
    return side1 * side2;
}*/
// findTarget
function findBox(ocrdata, pos) {
    pos.x = parseInt(pos.x);
    pos.y = parseInt(pos.y);
    for (var i = 0; i < ocrdata.regions.length; i++) {
        for (var j = 0; j < ocrdata.regions[i].lines.length; j++) {
            var box = BoxStr2ArrayInt(ocrdata.regions[i].lines[j].boundingBox);
            if ((box[0] < pos.x) && (box[1] < pos.y) && (box[2] > (pos.x - box[0])) && (box[3] > (pos.y - box[1]))) {
                return ocrdata.regions[i].lines[j];
            }
        }
        // box = BoxStr2ArrayInt(ocrdata.regions[i].boundingBox);
        // if ((box[0] < pos.x) && (box[1] < pos.y) && (box[2] > (pos.x - box[0])) && (box[3] > (pos.y - box[1]))) {
        //     return ocrdata.regions[i];
        // }
    }
    return;
}
// 解释执行mapping
function transform(ocrdata, mapping, data) {

    for (let l = 0; l < mapping.relation.length; l++) {
        var max = 0;
        var value = "";
        for (var i = 0; i < ocrdata.regions.length; i++) {
            if (mapping.relation[l].target == "line") {
                for (var j = 0; j < ocrdata.regions[i].lines.length; j++) {
                    var area = getOverlapbox(ocrdata.regions[i].lines[j].boundingBox, mapping.relation[l].box);
                    if (max < area) {
                        max = area;
                        value = ocrdata.regions[i].lines[j].lineContent;
                    }
                }

            }
            if (mapping.relation[l].target == "region") {
                area = getOverlapbox(ocrdata.regions[i].boundingBox, mapping.relation[l].box);
                if (area > 0) {
                    value = ocrdata.regions[i].regionContent;
                }
            }
        }
        data[mapping.relation[l].key] = value;
    }

}
export default { transform, BoxStr2ArrayInt, findBox }