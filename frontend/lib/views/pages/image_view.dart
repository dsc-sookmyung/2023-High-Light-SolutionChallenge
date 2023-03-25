import 'package:extended_image/extended_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

class ImageView extends StatefulWidget {
  final String url;

  const ImageView({Key? key, required this.url}) : super(key: key);

  @override
  _ImageViewState createState() => _ImageViewState();
}

class _ImageViewState extends State<ImageView> {

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            Container(
              padding: EdgeInsets.only(right: 40.w, bottom: 20.h),
              child: FloatingActionButton(
                backgroundColor: Colors.black,
                  onPressed: () {
                    Navigator.pop(context);
                  },
                child: Icon(
                  Icons.cancel_outlined,
                  color: Colors.white,
                  size: 80.w,
                ),
              ),
            ),
            SizedBox(height: 10.h,),
            Expanded(
                child: SizedBox(
                  width: double.infinity,
                  //color: Colors.redAccent,
                  child: InteractiveViewer(
                    child: ExtendedImage.network(
                      widget.url
                    ),
                  ),
                )
              ),
          ],
        ),
      ),
    );
  }
}


