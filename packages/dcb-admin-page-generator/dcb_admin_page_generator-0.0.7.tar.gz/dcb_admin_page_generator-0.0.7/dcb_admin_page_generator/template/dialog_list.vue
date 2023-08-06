<template>
    <z_dialog
        :visible="visible"
        :title="title"
        :append-to-body="appendToBody"
        :width="width"
        @update:visible="(val)=>{$emit('update:visible',val)}"
        @finish="dialogConfirm"
    >
      <z_page
        title="抽奖活动管理" :query-params.sync="queryParams"
        :table-option="table_option" :data="table_list" @press="press"/>
    <z_view_qr v-if="z_view_qr_visible" :visible.sync="z_view_qr_visible" :view-url="previewUrl"/>
    <!--  model_update  -->
    </z_dialog>
</template>

<script>
import Z_page from '@/components/Z/z_page';
import { zfTemplateDataDeal, zfTurnToTemplate,deepCopy } from '@/components/Z/z_funcs';
import { prepareFormData } from '@/x';
import Z_dialog_form from '@/components/Z/z_dialog_form';
import Z_view_qr from '@/components/Z/z_view_qr';
// Api writePlace

export default {
  name: 'index',
  components: { Z_view_qr, Z_dialog_form, Z_page },
  data() {
    return {
      change_edit_visible:false,
      z_view_qr_visible:false,
      queryParams: {
        fitter: [],
        pagination: {
          pageIndex: 1,
          pageSize: 10,
          total: 0,
        },
      },
      previewUrl: '',
      copyQueryParams: {},
      table_list: [{ test: '1' }],
      table_option: [],
      change_active_info: [],
      copy_change_active_info: [],
    };
  },
  async mounted() {
    await this.getDataList();
    this.copyQueryParams = deepCopy(this.queryParams);
    this.copy_change_active_info = deepCopy(this.change_active_info)
    this.tableOperationInit();
  },
  methods: {
    press(val) {
      if (val === 'add') {
        this.$router.push({ path: 'add_or_edit', query: {} });
        // this.changeActiveInfoReset()
        // this.change_edit_visible = true

      } else if (val === 'search') {
        this.getDataList();

      } else if (val === 'reset') {
        this.queryParamsReset();
      }
    },
    tableOperationInit() {
      const tp = {}
      let target_fpt_index = this.table_option.findIndex(ele => {
        return ele.type === 'op';
      });
      this.table_option[target_fpt_index].options.tableOperationList = {
        默认: [],
      };
      console.log('this.table_option[target_fpt_index]', this.table_option[target_fpt_index]);
    },
    queryParamsReset() {
      this.queryParams = deepCopy(this.copyQueryParams);
      this.getDataList();
    },
    changeActiveInfoReset(){
        this.change_active_info = deepCopy(this.copy_change_active_info)
    },
    async getDataList() {
      let temp_q = zfTemplateDataDeal(this.queryParams.fitter);
      temp_q = { ...temp_q, ...this.queryParams.pagination };
      const data = await SOMEFUNCS_LIST(temp_q);
      this.table_list = data.list;
      this.queryParams.pagination.total = data.total;
    },


    async changeFinish() {
      const temp_form = await prepareFormData(zfTemplateDataDeal(this.change_active_info));
      await SOMETHING_SUBMIT(temp_form);
      this.$message.success('操作成功');
      await this.getDataList()
      this.change_edit_visible = false;
    },
    async details(row) {
      this.changeActiveInfoReset()
      const res = await SOMEFUNCS_DETAIL({ id: row.id });
      this.change_active_info = zfTurnToTemplate(res, this.change_active_info);
      this.change_active_info = this.change_active_info.map(ele => {
        return { ...ele, options: { ...ele.options, disabled: true } };
      });
      this.change_edit_visible = true;
      console.log(row.id);
    },
    view(row) {
      this.previewUrl = row.previewUrl;
      this.z_view_qr_visible = true;
      console.log('row', row.previewUrl);
    },

    // 函数填充

  },
};
</script>

<style lang="scss" scoped>
.index {
  padding: 20px;
  background-color: rgb(240, 242, 245);
  position: relative;
  height: calc(100vh - 100px);
  overflow: auto;

  .wrap-padding-ct {
    position: relative;
    min-height: calc(100vh - 140px);
    background-color: #ffffff;
    padding: 20px;
  }
}
</style>
