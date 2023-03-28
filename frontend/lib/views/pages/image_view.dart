import 'package:extended_image/extended_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:photo_view/photo_view.dart';

class ImageView extends StatefulWidget {
  final String url;

  const ImageView({Key? key, required this.url}) : super(key: key);

  @override
  _ImageViewState createState() => _ImageViewState();
}

class _ImageViewState extends State<ImageView> {

  @override
  Widget build(BuildContext context) {
    print("image ${widget.url}");
    return Scaffold(
      body: Stack(
        fit: StackFit.expand,
        children: [
          ImageViewer(widget.url),
          Positioned(
            top: 10.h,
              right: 10.w,
              child: exitButton()
          )
        ],
      )
    );
  }

  Widget ImageViewer(String imageUrl){
    return Container(
      child: PhotoView(
        imageProvider: ExtendedNetworkImageProvider(imageUrl, cache: true,),
      ),
    );
  }

  Widget exitButton(){
    return Container(
      width: 70.w,
      height: 70.w,
      child: FloatingActionButton(
        backgroundColor: Colors.white,
        shape: StadiumBorder(
          side: BorderSide(color: Colors.black, width: 8),
        ),
        onPressed: () {
          Navigator.pop(context);
        },
        child: SvgPicture.asset(
          'assets/cancel_icon.svg',
          height: 40.h,
        )
        /*Icon(
          Icons.add,
          color: Colors.black,
          semanticLabel: "나가기",
          size: 64.w,
        ),*/
      ),
    );
  }
}


