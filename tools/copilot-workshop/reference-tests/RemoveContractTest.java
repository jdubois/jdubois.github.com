package com.juliendubois.workshop;

import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.assertThat;

class RemoveContractTest extends HttpFixture {
    @Test
    void removingTheLastItemReturnsAnEmptyCart() throws Exception {
        add(1, 2);
        var response = request("DELETE", "/api/cart/items/1", "");
        assertThat(response.statusCode()).isEqualTo(200);
        var body = json.readTree(response.body());
        assertThat(body.get("items").size()).isZero();
        assertThat(body.get("itemCount").asInt()).isZero();
        assertThat(body.get("totalCents").asInt()).isZero();
        assertThat(storedItems()).isZero();
    }

    @Test
    void removingOneProductPreservesOtherLinesAndTotals() throws Exception {
        add(1, 2);
        add(2, 3);
        var response = request("DELETE", "/api/cart/items/1", "");
        assertThat(response.statusCode()).isEqualTo(200);
        var body = json.readTree(response.body());
        assertThat(body.get("items").size()).isEqualTo(1);
        assertThat(body.get("items").get(0).get("productId").asLong()).isEqualTo(2);
        assertThat(body.get("items").get(0).get("quantity").asInt()).isEqualTo(3);
        assertThat(body.get("itemCount").asInt()).isEqualTo(3);
        assertThat(body.get("totalCents").asInt()).isEqualTo(3600);
        assertThat(storedItems()).isEqualTo(1);
        assertThat(storedQuantity(2)).isEqualTo(3);
    }

    @Test
    void removingAMissingLineReturns404WithoutChangingTheCart() throws Exception {
        assertThat(add(1, 1).statusCode()).isEqualTo(200);
        var before = cart();
        for (long productId : new long[] {2, 999}) {
            assertThat(request("DELETE", "/api/cart/items/" + productId, "").statusCode())
                    .as("missing cart line for product %s", productId).isEqualTo(404);
            assertThat(cart()).isEqualTo(before);
            assertThat(storedItems()).isEqualTo(1);
            assertThat(storedQuantity(1)).isEqualTo(1);
        }
    }
}
