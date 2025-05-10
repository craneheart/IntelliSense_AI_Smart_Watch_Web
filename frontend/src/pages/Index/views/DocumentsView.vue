<script setup>
import SideBar from "@/components/Sider/SideBar.vue";
import request from "@/api/request.js";
import {onMounted, reactive, ref} from "vue";
import {base64} from "@/ulits/File.js";

const DocNames = ref([]);
const Documents = reactive({});
const URL = '/documents/api/docs/'
const DocURL = ref(null)
const show = ref(false)

function getDocNames() {
  request.get(URL)
      .then((response) => {
        if (response.status === 200) {
          DocNames.value = response.data;
          changeDocShow(DocNames.value[0])
        } else {
          console.error("获取文档列表失败:", response.status);
        }
      })
      .catch((error) => {
        console.error("请求出错:", error);
      });
}

async function checkDocs(name) {
  if (!Documents[name]) {
    show.value = false
    const response = await request.post(URL, {name: name})
    const data = response.data
    Documents[name] = base64(data, "application/pdf")
    show.value = true
  }
}

async function changeDocShow(name) {
  await checkDocs(name)
  DocURL.value = Documents[name]
}

onMounted(() => {
  getDocNames()
})
</script>

<template>
  <div class="flex h-full w-full">
    <div class="flex-shrink-0">
      <SideBar :name-list="DocNames" :on-click="changeDocShow"/>
    </div>
    <div class="flex-grow h-screen relative p-0 m-0 flex items-center justify-center overflow-auto">
      <iframe
          v-if="show"
          :src="DocURL"
          class="w-full h-full min-h-[800px] border-0 block"
      ></iframe>
      <div v-else class="flex flex-col items-center justify-center">
        <div class="loading-spinner mb-4"></div>
        <p class="text-gray-500 text-lg">正在加载文档...</p>
      </div>
    </div>
  </div>
</template>
<style scoped>
.loading-spinner {
  width: 50px;
  height: 50px;
  border: 5px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: #3498db;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
