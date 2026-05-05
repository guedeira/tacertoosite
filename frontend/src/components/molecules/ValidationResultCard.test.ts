import { mount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";

import ValidationResultCard from "./ValidationResultCard.vue";

describe("ValidationResultCard", () => {
  it("renders a matching result", () => {
    const wrapper = mount(ValidationResultCard, {
      props: {
        result: {
          is_match: true,
          brand: "Google",
          official_domains: ["google.com"],
          submitted_domain: "google.com",
          message: "Domínio encontrado.",
        },
      },
    });

    expect(wrapper.text()).toContain("O link bate com o endereço oficial cadastrado.");
    expect(wrapper.text()).toContain("Domínio encontrado.");
  });

  it("renders official domains when there is no match", () => {
    const wrapper = mount(ValidationResultCard, {
      props: {
        result: {
          is_match: false,
          brand: "Google",
          official_domains: ["google.com", "gmail.com"],
          submitted_domain: "g00gle.com",
          message: "Domínio não encontrado.",
        },
      },
    });

    expect(wrapper.text()).toContain("Atenção");
    expect(wrapper.text()).toContain("google.com");
    expect(wrapper.text()).toContain("gmail.com");
  });
});

