class InfiniteScroll {
  constructor(options) {
    this.options = {...this.defaultOptions, ...options}
    this.container = document.querySelector(this.options.container);
    this.loading = document.querySelector(this.options.loading);
    this.more = document.querySelector(this.options.more);

    if (this.more) {
      this.setEventHandler();
    }
  }

  setEventHandler() {
    const html = document.querySelector('html');

    const handler = () => {
      if ((html.scrollTop + html.clientHeight >= html.scrollHeight) && this.loading.style.display !== 'block') {
        // show loading element
        this.loading.style.display = 'block';

        this.options.beforePageLoad();

        // get target page content
        this.getPageContent(this.more.href)
          .then((content) => {
            const data = this.parseStringToHtml(content);
            const items = data.querySelectorAll(this.options.item);
            const newMore = data.querySelector(this.options.more);

            // append received data to container
            items.forEach((item) => {
              this.container.append(item);
            });

            // replace new more href if it exist
            // else remove the old more element and remove the scroll event
            if (newMore) {
              this.more.href = newMore.href;
            } else {
              this.more.remove();
              document.removeEventListener('scroll', handler);
            }

            this.options.afterPageLoad(items);
            this.loading.style.display = 'none';
          });
      }
    }

    handler();
    document.addEventListener('scroll', handler);
  }

  getPageContent(link) {
    return new Promise((resolve) => {
      fetch(link)
        .then((res) => {
          return res.text();
        })
        .then((content) => {
          resolve(content);
        })
        .catch((err) => {
          toast.fire({
            title: 'مشکلی در لود شدن اطلاعات وجود دارد!',
            icon: 'error',
          });
        });
    });
  }

  parseStringToHtml(string) {
    const parser = new DOMParser();
    return parser.parseFromString(string, 'text/html');
  }

  defaultOptions = {
    container: '.infinite-container',
    more: '.infinite-more-link',
    loading: '.infinite-loading',
    item: '.infinite-item',
    beforePageLoad() {
    },
    afterPageLoad() {
    },
  }
}
