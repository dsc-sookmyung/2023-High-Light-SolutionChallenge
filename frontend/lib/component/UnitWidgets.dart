import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

import '../models/imageUnit.dart';

Widget textBlock(List<dynamic> _allTexts,int fontBase, int idx){
  return InkWell(
    highlightColor: Colors.amberAccent,
    splashColor: Colors.amberAccent,
    onTap: (){
      setState(){

      }
    },
    child: Container(
      //color: Colors.orange,
      child: Text(
        _allTexts[idx].textLine,
        style: TextStyle(
            fontSize:
            _allTexts[idx].fontSize.toDouble() + fontBase),
      ),
    ),
  );
}

Widget textListView(List<dynamic> _allTexts, int fontBase, bool spacer) {
  return Container(
    //height: double.infinity,
    child: ListView.builder(
        itemCount: _allTexts.length,
        itemBuilder: (ctx, int idx) {
          if ((idx == _allTexts.length-1) && spacer) {
            //print(spacer);
            return Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                textBlock(_allTexts, fontBase, idx),
                Container(
                  //color:Colors.amber,
                  height: 110.h,
                  width: 200.w,
                ),
              ],
            );
          }
          return textBlock(_allTexts, fontBase, idx);
        }),
  );
}

Widget imgWidget(List<ImageUnit>? allImages) {
  return Container(
    decoration: BoxDecoration(
      borderRadius: BorderRadius.only(
          topLeft: Radius.circular(30.w), topRight: Radius.circular(30.w)),
      color: Color(0x4d666666),
    ),
    child: ListView.builder(
        scrollDirection: Axis.horizontal,
        itemCount: allImages!.length,
        itemBuilder: (ctx, int idx) {
          return Container(
              margin: EdgeInsets.fromLTRB(20.w, 10.h, 30.w, 10.h),
              child: Image.asset(
                allImages![idx].imgUrl,
                width: 100.w,
                height: 100.h,
                fit: BoxFit.fill,
              ));
        }),
  );
}
