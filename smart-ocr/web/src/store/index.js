import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

//挂载Vuex
Vue.use(Vuex)

//创建VueX对象
const store = new Vuex.Store({
  state: {
    //存放的键值对就是所要管理的状态
    loading: true,
    dataModelList: [],
    chosedDataModel: '',// 0 means New DataModel
    DataModel: {
      data: {

      }
    },
    mapping: {
      "relation": []
    }

  },
  getters: {
    uploadUrl: state => {
      return "/uploadUrl/" + state.chosedDataModel;
    }
  },
  mutations: {
    setDataModel(state, payload) {
      //state.DataModel.data[payload.key] = payload.value;
      //响应式添加属性，参见https://cn.vuejs.org/v2/guide/reactivity.html#检测变化的注意事项
      Vue.set(state.DataModel.data, payload.key, payload.value);
    },
    delDataModel(state, payload) {
      //响应式删除属性，参见https://cn.vuejs.org/v2/api/#Vue-delete
      Vue.delete(state.DataModel.data, payload.key);
    },
    addmapping(state, payload) {
      // {key:state.DataModel.data[payload.key],box:"263,99,485,99,485,137,263,137"}
      var relation = state.mapping.relation.filter((r) => {
        return r.key == payload.key;
      });
      console.log("relation:" + relation);
      if (relation.length > 0) {
        var index = state.mapping.relation.indexOf(relation[0]);
        state.mapping.relation[index].box = payload.box;
        state.mapping.relation[index].target = payload.target;
      } else {
        state.mapping.relation.push(payload);
      }
      console.log(state.mapping.relation);
    },
    getDataModelList(state, list) {
      state.dataModelList = list;
    },
    changeDataModel(state, DataModel) {
      state.DataModel = DataModel.DataModel;
      state.mapping = DataModel.mapping;
    },
    chooseDataModel(state, id) {
      state.chosedDataModel = id;
      state.loading = false;
    },

  },
  actions: {
    saveDataModel(context) {
      return new Promise((resolve, reject) => {
        console.log(context);
        var m = context.state.dataModelList.filter((r) => {
          return r.id == context.state.chosedDataModel;
        });
        console.log(m)
        axios.post('/saveDataModel', {
          "id": context.state.chosedDataModel,
          "name": m[0].label,
          "DataModel": context.state.DataModel,
          "mapping": context.state.mapping
        })
          .then(function (response) {
            console.log(response.data.dataModelList.length);
            if (context.state.chosedDataModel == 0) {
              context.commit("chooseDataModel", response.data.dataModelList[response.data.dataModelList.length - 1].id);
            }
            context.commit("getDataModelList", response.data.dataModelList);
            resolve();
          })
          .catch(function () {
            console.log("saveDataModel error");
            reject();
          });
      })
    },
    getDataModelList(context) {
      axios.get('/getDataModelList')
        .then(function (response) {
          console.log(response.data);
          context.commit("getDataModelList", response.data.dataModelList);
          context.dispatch("getDataModel", response.data.dataModelList[0].id);
        })
        .catch(function (error) {
          console.log(error);
          context.commit("getDataModelList", [{ id: "0", label: "default" }]);
          context.dispatch("getDataModel", 0);
        });

    },
    getDataModel(context, id) {
      if (id == 0) {
        context.commit("chooseDataModel", id);
        context.commit("changeDataModel", {
          DataModel: {
            data: {
              "default": "value"
            }
          },
          mapping: {
            "relation": []
          }
        });
        return;
      }
      axios.get('/models/' + id)
        .then(function (response) {
          console.log(response.data);
          context.commit("chooseDataModel", id);
          context.commit("changeDataModel", response.data);
        })
        .catch(function (error) {
          console.log(error);
        })
    },
    rmDataModel(context, id) {
      console.log(id);
      axios.get('/rm_models/' + id)
        .then(function (response) {
          console.log(response);
          context.dispatch("getDataModelList");
        })

    }
  },
})

export default store