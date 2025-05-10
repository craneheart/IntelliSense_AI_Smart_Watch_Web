<template>
  <div class="relative h-full overflow-hidden">
    <div
        :class="[
        cn(
          'flex cursor-pointer items-center gap-1 rounded-md text-sm',
          isSelect && isSelectable ? 'bg-muted' : '',
          !isSelectable ? 'cursor-not-allowed opacity-50' : '',
          $props.class,
        ),
      ]"
        :dir="direction"
        class="flex cursor-pointer items-center gap-1 rounded-md text-sm transition-all duration-200"
        @click="onTriggerClick"
    >
      <Icon
          v-if="isExpanded"
          :name="openIcon"
          size="16"
      />
      <Icon
          v-else
          :name="closeIcon"
          size="16"
      />

      <span class="select-none">{{ name }}</span>
    </div>

    <div
        v-if="isExpanded"
        class="relative text-sm"
    >
      <TreeIndicator
          v-if="name && indicator"
          aria-hidden="true"
      />
      <div
          :dir="direction"
          class="ml-5 flex flex-col gap-1 py-1 rtl:mr-5"
      >
        <slot/>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {cn} from "@/lib/utils";
import {type FolderProps, TREE_CONTEXT_SYMBOL, type TreeContextProps} from "./index";
import {computed, inject, toRefs} from "vue";

const props = withDefaults(defineProps<FolderProps>(), {
  isSelectable: true,
});

const {id, name, isSelectable, isSelect} = toRefs(props);

const treeContext = inject<TreeContextProps>(TREE_CONTEXT_SYMBOL);
if (!treeContext) {
  throw new Error("[Folder] must be used inside <Tree>");
}

const {expandedItems, handleExpand, openIcon, closeIcon, direction, indicator} = treeContext;

const isExpanded = computed<boolean>(() => {
  return !!expandedItems.value?.includes(id.value);
});

function onTriggerClick() {
  if (!isSelectable.value) return;
  handleExpand(id.value);
}
</script>