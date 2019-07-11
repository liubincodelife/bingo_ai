// pages/classification/classification.js
const app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
      title: '表情识别',
      bgPic: null,
      emptyPic: '/images/classification.jpg',
      emotionClass: 0,
      confidence: null,
      markFile: null,
      markPic: null,
      downloadPath: null,
      picChoosed: false,
      actionSheetHidden: true,
      actionSheetItems: ['拍照', '从相册选择']
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
      if (app.globalData.userInfo) {
          this.setData({
              //bgPic: app.globalData.userInfo.avatarUrl,
              picChoosed: false
          })
      } else {
          // 在没有 open-type=getUserInfo 版本的兼容处理
          wx.getUserInfo({
              success: res => {
                  app.globalData.userInfo = res.userInfo;
                  this.setData({
                      userInfo: res.userInfo,
                      bgPic: res.userInfo.avatarUrl,
                      emotionClass: 0
                  });
                  this.assignPicChoosed();
              }
          })
      }
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },

    
    actionSheetTap: function () {
        var itemList = ['拍照', '从相册选择'];
        var that = this;
        wx.showActionSheet({
            itemList: itemList,
            //itemColor: '#007aff',
            success(res) {
                
                if (res.tapIndex == 0) {
                    console.log("点击拍照");
                    wx.chooseImage({
                        count: 1,
                        sizeType: ["original", "compressed"], // 可以指定是原图还是压缩图，默认二者都有
                        sourceType: ['camera'], // 可以指定来源是相册还是相机，默认二者都有  
                        success: (res) => {
                            var tempFilePaths = res.tempFilePaths;
                            that.setData({
                                bgPic: res.tempFilePaths[0]
                            });
                            that.assignPicChoosed();
                        },
                        fail: (res) => {
                            that.assignPicChoosed();
                        },
                        complete: (res) => {
                            that.assignPicChoosed();
                        },
                    })
                }
                else if (res.tapIndex == 1){
                    console.log("点击相册");
                    wx.chooseImage({
                        count: 1,
                        sizeType: ["original", "compressed"], // 可以指定是原图还是压缩图，默认二者都有
                        sourceType: ['album'], // 可以指定来源是相册还是相机，默认二者都有  
                        success: (res) => {
                            var tempFilePaths = res.tempFilePaths;
                            that.setData({
                                bgPic: res.tempFilePaths[0]
                            });
                            that.assignPicChoosed();
                        },
                        fail: (res) => {
                            that.assignPicChoosed();
                        },
                        complete: (res) => {
                            that.assignPicChoosed();
                        },
                    })
                }

            },
            fail(res) {
                console.log(res.errMsg)
            }
        })
    },

    /**
     * 上传图片，处理完成后切换到分类结果显示界面
     */
    uploadTap: function (e) {
        var that = this;
        //将选择的图片作为全局数据
        app.globalData.bgPic = that.data.bgPic;
        wx.showToast({
            title: '正在处理', icon: 'loading', duration: 100000
        });
        console.log("start upload : ", that.data.bgPic)
        wx.uploadFile({
            //url: 'http://107.167.188.242:5000/classification',
            url: 'https://bingoai.com.cn:5000/classification',
            filePath: that.data.bgPic,
            name: 'file',
            header: {
                'content-type': 'multipart/form-data'
            },
            // 设置请求的 header
            //...
            success: function (res) {
                console.log(res.data);
                wx.hideToast();
                if (res.statusCode == 200) {
                    var jsonStr = JSON.parse(res.data);//将json字符串转为json对象
                    console.log('200');
                    var retCode = jsonStr["code"];
                    if(retCode == 1) {
                        wx.showModal({
                            title: '提示',
                            content: '请上传正脸照片',
                            success(res) {
                                if (res.confirm) {
                                    console.log('用户点击确定')
                                } else if (res.cancel) {
                                    console.log('用户点击取消')
                                }
                            }
                        })
                    }
                    else{
                        app.globalData.emotionClass = jsonStr["emotion"];
                        app.globalData.confidence = jsonStr["confidence"];
                        app.globalData.markFile = jsonStr["filename"]
                        that.data.emotionClass = app.globalData.emotionClass;
                        that.data.confidence = app.globalData.confidence;
                        that.data.markFile = app.globalData.markFile;
                        console.log(app.globalData.emotionClass);
                        console.log(app.globalData.confidence);
                        console.log(app.globalData.markFile);
                        that.data.downloadPath = "https://bingoai.com.cn:5000/download/" + that.data.markFile;
                        console.log(that.data.downloadPath);
                        wx.downloadFile({
                            url: that.data.downloadPath,
                            success: function (res) {
                                console.log("download success");
                                console.log(res.tempFilePath);
                                app.globalData.markPic = res.tempFilePath;
                                that.data.markPic = app.globalData.markPic;
                                console.log(that.data.markPic);
                                wx.navigateTo({
                                    url: '../showEmotionResult/showEmotionResult',
                                })
                            }
                        }) 
                    }                 
                } else {
                    wx.showModal({
                        title: '提示',
                        content: '服务器错误，请稍后重试！',
                    });
                }
            },
            fail: function (res) {
                console.log(res);
            }
        })
    },

    assignPicChoosed() {    // userInfo被赋值后调用的过程
        if (this.data.bgPic) {
            this.setData({
                picChoosed: true
            })
        } else {
            this.setData({
                picChoosed: false
            })
        }
    },
    /**
     * 选择图片
     */
    chooseImage(from) {
        wx.chooseImage({
            count: 1,
            sizeType: ["original", "compressed"], // 可以指定是原图还是压缩图，默认二者都有
            sourceType: [from.target.dataset.way],
            // sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有  
            success: (res) => {
                var tempFilePaths = res.tempFilePaths;
                this.setData({
                    bgPic: res.tempFilePaths[0]
                });
                this.assignPicChoosed();
            },
            fail: (res) => {
                this.assignPicChoosed();
            },
            complete: (res) => {
                this.assignPicChoosed();
            },
        })
    },
  
})