var app = new Vue({
    el: "#app",
    data: {
      data: [
        {
          name: "巧呼呼蘇打水",
          price: 30,
          expiryDate: 90
        },
        {
          name: "心驚膽跳羊肉飯",
          price: 65,
          expiryDate: 2
        },
        {
          name: "郭師傅武功麵包",
          price: 32,
          expiryDate: 1
        },
        {
          name: "不太會過期的新鮮牛奶",
          price: 75,
          expiryDate: 600
        },
        {
          name: "金殺 巧粒粒",
          price: 120,
          expiryDate: 200
        }
      ],
      sortType: "price",
      isReverse: false
    },
    // 請在此撰寫 JavaScript
    methods: {
      changeType: function (type) {
        var vm = this;
        if (vm.sortType == type) {
          vm.isReverse = !vm.isReverse;
        } else {
          vm.isReverse = false;
        }
        vm.sortType = type;
      }
    },
    computed: {
      sortData() {
        var vm = this;
        var type = vm.sortType;
        return vm.data.sort(function (a, b) {
          if (vm.isReverse) return b[type] - a[type];
          else return a[type] - b[type];
        });
      }
    }
  });