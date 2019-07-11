// pages/home/home.js
//获取应用实例
const $vm = getApp()
const cache = Object.create(null)
Page({

  /**
   * 页面的初始数据
   */
  data: {

  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this;
    // 高度自适应
    wx.getSystemInfo({
      success: function (res) {
        var clientHeight = res.windowHeight,
          clientWidth = res.windowWidth,
          rpxR = 750 / clientWidth;
        var calc = clientHeight * rpxR;
        that.setData({
          winHeight: calc,
        });
      }
    });

    // 打开调试，不进行域名检查
    wx.setEnableDebug({
        enableDebug: true
    })
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

  classificationBtnClick:function(e) {
    wx.navigateTo({
      url: '../classification/classification',
    })
  },

  segmentationBtnClick: function (e) {
    //wx.navigateTo({
    //  url: '../segmentation/segmentation',
    //})
      wx.showToast({
          title: '敬请期待', icon: 'none', duration: 2000
      });
  },

  detectionBtnClick: function (e) {
    //wx.navigateTo({
    //  url: '../detection/detection',
    //})
      wx.showToast({
          title: '敬请期待', icon: 'none', duration: 2000
      });
  },
})