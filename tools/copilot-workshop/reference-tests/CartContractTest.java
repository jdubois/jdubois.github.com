package com.juliendubois.workshop;

import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.assertThat;

class CartContractTest extends HttpFixture {
    @Test
    void repeatedAddIncrementsQuantityAndTotal() throws Exception {
        assertThat(add(1, 1).statusCode()).isEqualTo(200);
        var response = add(1, 1);
        assertThat(response.statusCode()).isEqualTo(200);
        var body = json.readTree(response.body());
        assertThat(body.get("items").size()).isEqualTo(1);
        assertThat(body.get("items").get(0).get("quantity").asInt()).isEqualTo(2);
        assertThat(body.get("items").get(0).get("lineTotalCents").asInt()).isEqualTo(2000);
        assertThat(body.get("itemCount").asInt()).isEqualTo(2);
        assertThat(body.get("totalCents").asInt()).isEqualTo(2000);
        assertThat(storedQuantity(1)).isEqualTo(2);
    }

    @Test
    void addingSeveralUnitsKeepsOneLine() throws Exception {
        add(1, 3);
        assertThat(add(1, 2).statusCode()).isEqualTo(200);
        var body = cart();
        assertThat(body.get("items").size()).isEqualTo(1);
        assertThat(body.get("totalCents").asInt()).isEqualTo(5000);
        assertThat(storedQuantity(1)).isEqualTo(5);
    }

    @Test
    void exceedingTheLimitPreservesExistingQuantity() throws Exception {
        add(1, 99);
        assertThat(add(1, 1).statusCode()).isEqualTo(400);
        assertThat(storedQuantity(1)).isEqualTo(99);
        assertThat(cart().get("totalCents").asInt()).isEqualTo(99000);
    }
}
