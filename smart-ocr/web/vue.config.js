 module.exports = {

  devServer: {
    proxy: {
      '/uploadUrl': {
        target: `http://172.16.96.167:8080/uploadUrl`,
        changeOrigin: true,
        pathRewrite: {
          '^/uploadUrl' : ''
        }
      }

}
}
}