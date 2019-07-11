// pages/showEmotionResult/showEmotionResult.js
const app = getApp();
Page({

    /**
     * 页面的初始数据
     */
    data: {
        title: '识别结果',
        featureImg:null,
        emotionClass:null,
        confidence:null
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        if (app.globalData.userInfo) {
            this.setData({
                featureImg: app.globalData.markPic,
                emotionClass: app.globalData.emotionClass,
                confidence:app.globalData.confidence
            })
            
        } else {
            // 在没有 open-type=getUserInfo 版本的兼容处理
            wx.getUserInfo({
                success: res => {
                    this.setData({
                        featureImg: app.globalData.bgPic,
                        emotionClass: app.globalData.emotionClass,
                        confidence: app.globalData.confidence
                    });
                }
            })
        }
        console.log(this.data.emotionClass);
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

    }
})