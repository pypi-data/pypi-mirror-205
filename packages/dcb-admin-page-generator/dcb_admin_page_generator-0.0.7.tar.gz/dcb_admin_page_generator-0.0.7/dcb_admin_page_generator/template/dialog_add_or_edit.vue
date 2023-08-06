<template>
    <z_dialog_form
      ref="z_dialog_form"
      title="抽奖活动管理"
      v-if="visible"
      :visible="visible"
      append-to-body
      v-model="change_active_info"
      @update:visible="(val)=>{ $emit('update:visible',val) }"
      @finish="(func)=>{ $emit('finish',func) }"
      label-width="150px" width="80%" title="场次信息"/>
</template>

<script>
import Z_dialog_form from '@/components/Z/z_dialog_form';
import { zfTemplateDataDeal } from '@/components/Z/z_funcs';
import { prepareFormData } from '@/x';
// Api writePlace


export default {
  name: 'add_or_edit_step_1',
  components: { Z_dialog_form },
  props:{
   visible:{
      default:false,
      type:Boolean
    },
  },
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
