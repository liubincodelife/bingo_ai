// pages/detection/detection.js
const app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
      title: '目标检测',
      bgPic: null,
      aestheticscore: 0,
      picChoosed: false,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

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

    /**
    * 返回首页
    */
    backBtnClick: function (e) {
        wx.navigateBack({
            delta: 1
        })

    },
    /**
     * 下一步,跳到保存分享页
     */
    nextPageBtnClick: function (e) {
        var that = this;
        //将选择的图片作为全局数据
        app.globalData.bgPic = that.data.bgPic;
        wx.showToast({
            title: '正在处理', icon: 'loading', duration: 100000
        });
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