(() => {
  const SITE = {
    date_iso: "2027-10-08T16:00:00-07:00",
    en: {
      couple: ["Michael", "Janice"],
      eyebrow: "Save the date",
      date: "Friday, October 8, 2027",
      place: "San Francisco",
      countdown: "days to go",
      when_label: "When", when: "Friday, October 8, 2027",
      where_label: "Where", where: "The Log Cabin at the Presidio", where_sub: "San Francisco, California",
      closing: "We can't wait to celebrate with you.",
      soon: "RSVP coming soon.",
    },
    ko: {
      couple: ["이진섭", "이나현"],
      eyebrow: "초대합니다",
      date: "2027년 10월 8일 금요일",
      place: "샌프란시스코",
      countdown: "", // Korean uses the D-day convention instead, e.g. D-355
      footer: "신랑 이진섭 · 신부 이나현",
      when_label: "일시", when: "2027년 10월 8일 금요일",
      where_label: "장소", where: "The Log Cabin at the Presidio", where_sub: "샌프란시스코, 캘리포니아",
      closing: "소중한 분들과 함께 그날을 맞이하고 싶습니다.",
      soon: "참석 여부는 청첩장과 함께 다시 여쭙겠습니다.",
    },
  };
  const $ = (s) => document.querySelector(s);
  const esc = (s) => String(s).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
  let lang = localStorage.getItem("std_lang") || ((navigator.language || "").toLowerCase().startsWith("ko") ? "ko" : "en");

  function render() {
    const t = SITE[lang];
    document.documentElement.lang = lang;
    localStorage.setItem("std_lang", lang);
    document.querySelectorAll("[data-t]").forEach((el) => { if (t[el.dataset.t] != null) el.textContent = t[el.dataset.t]; });
    $("#names").innerHTML = `${esc(t.couple[0])} <em>&amp;</em> ${esc(t.couple[1])}`;
    $("#footer-names").textContent = t.footer || t.couple.join(" & ");
    document.title = `${t.eyebrow} · ${t.couple.join(" & ")}`;
    document.querySelectorAll(".lang button").forEach((b) => b.classList.toggle("on", b.dataset.lang === lang));
  }
  function tick() {
    const ms = new Date(SITE.date_iso).getTime() - Date.now();
    const days = Math.max(0, Math.ceil(ms / 86400000));
    $("#days").textContent = lang === "ko" ? `D-${days}` : String(days);
  }
  document.querySelector(".lang").addEventListener("click", (e) => {
    const b = e.target.closest("button[data-lang]"); if (b && b.dataset.lang !== lang) { lang = b.dataset.lang; render(); tick(); }
  });
  const nav = document.querySelector(".nav");
  const onScroll = () => nav.classList.toggle("scrolled", window.scrollY > 40);
  window.addEventListener("scroll", onScroll, { passive: true });
  render(); tick(); setInterval(tick, 60000); onScroll();
})();
