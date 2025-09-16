<template>
  <div class="calendar-container">
    <div class="header">
      <button @click="prevMonth">&lt;</button>
      <h2>{{ currentMonthDisplay }}</h2>
      <button @click="nextMonth">&gt;</button>
    </div>
    <div class="days-of-week">
      <div v-for="day in daysOfWeek" :key="day">{{ day }}</div>
    </div>
    <div class="dates">
      <div
        v-for="date in calendarDates"
        :key="date.iso"
        :class="{'date-cell': true, 'current-month': date.isCurrentMonth, 'selected': date.isSelected }"
        @click="selectDate(date)"
      >
        {{ date.day }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineEmits } from 'vue';
import { format, getDay, startOfMonth, endOfMonth, eachDayOfInterval, addMonths, subMonths, addDays, subDays } from 'date-fns';
import { ja } from 'date-fns/locale';

/**
 * @typedef {Object} CalendarDate
 * @property {string} iso - 日付のISO 8601形式（'YYYY-MM-DD'）。
 * @property {string} day - 日付の数字部分。
 * @property {boolean} isCurrentMonth - 表示中の月の日付かどうか。
 * @property {boolean} isSelected - 現在選択されている日付かどうか。
 */

const emit = defineEmits(['date-selected', 'month-changed']);

/**
 * 曜日を表示するための配列。
 * @type {string[]}
 */
const daysOfWeek = ['日', '月', '火', '水', '木', '金', '土'];
/**
 * 現在の日付の参照。
 * @type {import('vue').Ref<Date>}
 */
const today = ref(new Date());
/**
 * 現在表示されている月の開始日の参照。
 * @type {import('vue').Ref<Date>}
 */
const currentMonth = ref(startOfMonth(today.value));
/**
 * 選択された日付の参照。
 * @type {import('vue').Ref<Date | null>}
 */
const selectedDate = ref(null);

/**
 * 現在表示されている月の表示名（例: '2025年09月'）。
 * @type {import('vue').ComputedRef<string>}
 */
const currentMonthDisplay = computed(() => {
  return format(currentMonth.value, 'yyyy年MM月', { locale: ja });
});

/**
 * カレンダーに表示するすべての日付を生成する算出プロパティ。
 * 前月と翌月の日付を含めて、常に6週間分（42日分）のカレンダーを生成します。
 * @returns {CalendarDate[]}
 */
const calendarDates = computed(() => {
  const startDayOfMonth = startOfMonth(currentMonth.value);
  const endDayOfMonth = endOfMonth(currentMonth.value);

  // カレンダーの開始日を決定（日曜日から開始）
  const calendarStart = subDays(startDayOfMonth, getDay(startDayOfMonth));
  // カレンダーの終了日を決定（土曜日で終了）
  const calendarEnd = addDays(endDayOfMonth, 6 - getDay(endDayOfMonth));

  const allDates = eachDayOfInterval({ start: calendarStart, end: calendarEnd });

  return allDates.map(date => {
    return {
      iso: format(date, 'yyyy-MM-dd'),
      day: format(date, 'd'),
      isCurrentMonth: format(date, 'MM') === format(currentMonth.value, 'MM'),
      isSelected: selectedDate.value && format(date, 'yyyy-MM-dd') === format(selectedDate.value, 'yyyy-MM-dd'),
    };
  });
});

/**
 * 前の月に移動し、親コンポーネントに通知します。
 */
const prevMonth = () => {
  currentMonth.value = subMonths(currentMonth.value, 1);
  emit('month-changed', format(currentMonth.value, 'yyyy-MM'));
};

/**
 * 次の月に移動し、親コンポーネントに通知します。
 */
const nextMonth = () => {
  currentMonth.value = addMonths(currentMonth.value, 1);
  emit('month-changed', format(currentMonth.value, 'yyyy-MM'));
};

/**
 * 日付が選択されたときに実行されます。
 * 当月の日付のみ選択可能です。
 * @param {CalendarDate} dateObj - 選択された日付オブジェクト。
 */
const selectDate = (dateObj) => {
  if (dateObj.isCurrentMonth) {
    selectedDate.value = new Date(dateObj.iso);
    emit('date-selected', dateObj.iso);
  }
};
</script>

<style scoped>
.calendar-container {
  font-family: Arial, sans-serif;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 1rem;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 300px;
  margin-bottom: 2rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.header button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}

.header h2 {
  font-size: 1.2rem;
  margin: 0;
}

.days-of-week {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  text-align: center;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.dates {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  text-align: center;
}

.date-cell {
  padding: 0.5rem;
  cursor: pointer;
  border-radius: 4px;
}

.date-cell.current-month {
  color: #333;
}

.date-cell:not(.current-month) {
  color: #ccc;
}

.date-cell.selected {
  background-color: #42b983;
  color: #fff;
  font-weight: bold;
}
</style>