<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  title:      { type: String,  required: true },
  fields:     { type: Array,   required: true },
  modelValue: { type: Object,  default: () => ({}) },
  isEdit:     { type: Boolean, default: false },
  error:      { type: String,  default: '' },
})

const emit = defineEmits(['submit', 'close'])

const formData = ref({})

watch(
  () => props.modelValue,
  (val) => { formData.value = { ...(val || {}) } },
  { immediate: true, deep: true }
)

const visibleFields = computed(() =>
  props.fields.filter(f => !(f.createOnly && props.isEdit))
)

function handleSubmit() {
  emit('submit', { ...formData.value })
}
</script>

<template>
  <Teleport to="body">
    <div
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
      @mousedown.self="$emit('close')"
    >
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] flex flex-col">

        <!-- Header -->
        <div class="flex items-center justify-between px-6 py-4 border-b border-gray-100">
          <h2 class="text-base font-semibold text-gray-800">{{ title }}</h2>
          <button
            @click="$emit('close')"
            class="w-7 h-7 flex items-center justify-center rounded-full text-gray-400 hover:bg-gray-100 hover:text-gray-600 transition-colors text-lg leading-none"
          >×</button>
        </div>

        <!-- Body -->
        <div class="overflow-y-auto flex-1 px-6 py-5">
          <div
            v-if="error"
            class="mb-4 px-4 py-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm"
          >
            {{ error }}
          </div>

          <div class="grid grid-cols-2 gap-x-5 gap-y-4">
            <div
              v-for="field in visibleFields"
              :key="field.key"
              :class="field.fullWidth ? 'col-span-2' : ''"
            >
              <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">
                {{ field.label }}
                <span v-if="field.required" class="text-red-400 normal-case font-normal ml-0.5">*</span>
              </label>

              <!-- Select -->
              <select
                v-if="field.type === 'select'"
                v-model="formData[field.key]"
                :required="field.required"
                :disabled="field.readOnly"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:text-gray-500"
              >
                <option :value="null">— не выбрано —</option>
                <option
                  v-for="opt in (field.options || [])"
                  :key="opt.value"
                  :value="opt.value"
                >{{ opt.label }}</option>
              </select>

              <!-- Checkbox -->
              <div v-else-if="field.type === 'checkbox'" class="flex items-center gap-2 mt-1">
                <input
                  type="checkbox"
                  v-model="formData[field.key]"
                  class="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span class="text-sm text-gray-600">{{ field.checkLabel || '' }}</span>
              </div>

              <!-- Textarea -->
              <textarea
                v-else-if="field.type === 'textarea'"
                v-model="formData[field.key]"
                :required="field.required"
                :disabled="field.readOnly"
                :placeholder="field.placeholder || ''"
                rows="3"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none disabled:bg-gray-100"
              />

              <!-- Default input -->
              <input
                v-else
                :type="field.type || 'text'"
                v-model="formData[field.key]"
                :required="field.required"
                :disabled="field.readOnly"
                :placeholder="field.placeholder || ''"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:text-gray-500"
              />
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="flex justify-end gap-3 px-6 py-4 border-t border-gray-100">
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 py-2 text-sm text-gray-600 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          >Отмена</button>
          <button
            type="button"
            @click="handleSubmit"
            class="px-5 py-2 text-sm text-white bg-blue-600 hover:bg-blue-700 active:bg-blue-800 rounded-lg transition-colors font-medium"
          >{{ isEdit ? 'Сохранить' : 'Создать' }}</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>
