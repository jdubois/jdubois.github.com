package com.juliendubois.workshop;

import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.assertThat;

class QueryContractTest extends HttpFixture {
    @Test
    void eightDistinctProductsUseOneSelect() throws Exception { checkCart(8); }

    @Test
    void doublingTheCartDoesNotGrowTheSelectBudget() throws Exception { checkCart(16); }

    private void checkCart(int count) throws Exception {
        seed.reset(count);
        statistics().clear();
        var body = cart();
        long statements = statistics().getPrepareStatementCount();
        assertThat(body.size()).isEqualTo(3);
        assertThat(body.get("items").size()).isEqualTo(count);
        int expectedTotal = 0;
        for (int i = 0; i < count; i++) {
            var item = body.get("items").get(i);
            int price = i == 0 ? 1000 : 1000 + (i + 1) * 100;
            assertThat(item.size()).isEqualTo(5);
            assertThat(item.get("productId").asLong()).isEqualTo(i + 1);
            assertThat(item.get("name").asString()).isNotBlank();
            assertThat(item.get("priceCents").asInt()).isEqualTo(price);
            assertThat(item.get("quantity").asInt()).isEqualTo(1);
            assertThat(item.get("lineTotalCents").asInt()).isEqualTo(price);
            expectedTotal += price;
        }
        assertThat(body.get("items").get(0).get("name").asString()).isEqualTo("Notebook");
        assertThat(body.get("itemCount").asInt()).isEqualTo(count);
        assertThat(body.get("totalCents").asInt()).isEqualTo(expectedTotal);
        assertThat(statements).as("completed HTTP cart SELECTs").isEqualTo(1);
    }
}
