<template>
  <div class="add_or_edit">
    <div class="add_or_edit_ct">
        <!--      <x-steps :steps="['创建活动','奖品管理','活动规则设置','创建完成']" :current="active_step"/>-->
        <z_form ref="z_form" v-model="change_active_info" width="800px" label-width="120px"/>
    </div>
    <div class="page-footer">
      <el-button v-if="active_step === 0" @click="$router.push({ path: 'index', query: {} })">取消</el-button>
      <el-button v-else @click="active_step-=1">上一步</el-button>
      <el-button v-if="active_step !== 2" type="primary" @click="nextStep">下一步</el-button>
      <el-button v-loading="loading" v-else type="primary" @click="submit">提交</el-button>
    </div>
  </div>
</template>

<script>
import Z_form from '@/components/Z/z_form';
import { zfTemplateDataDeal } from '@/components/Z/z_funcs';
import { prepareFormData } from '@/x';
// Api writePlace


export default {
  name: 'add_or_edit_step_1',
  components: { Z_form },
  data() {
    return {
      loading:false,
      active_step:0,
      change_active_info: [],
    };
  },
  methods: {
    validate(func) {
      this.$refs.z_form.validate(func);
    },
    getValue() {
      const data = zfTemplateDataDeal(this.change_active_info);
      console.log('data1', data);
      return data;
    },
    nextStep(){},
    async submit(){
        this.$refs.z_form.validate(async (val) => {
            if(val){
                let data = zfTemplateDataDeal(this.change_active_info);
                data = await prepareFormData(data);
                await SOMETHING_SUBMIT(data).then(() => {
                    this.$message.success('新增成功');
                    this.$router.push({ path: 'index', query: {} });
                }).finally(() => {
                    this.loading = false;
                })
            }
            else{
            }
        })
    },
    // 函数填充
  },
};
</script>

<style lang="scss" scoped>
.add_or_edit {
  padding: 20px;
  background-color: rgb(240, 242, 245);
  position: relative;
  height: calc(100vh - 100px);
  overflow: auto;

  &_ct {
    position: relative;
    height: calc(100vh - 200px);
    overflow: auto;
    background-color: #ffffff;
    padding: 20px 20px 60px 20px;
    width: 100%;

  }
  .page-footer {
    height: 60px;
    padding: 10px;
    display: flex;
    justify-content: center;
    width: 100%;
    background-color: #ffffff;
    border: 1px solid #eeefff;
    box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);;
  }

}


</style>
