# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import Union
from datetime import datetime
from typing_extensions import Literal

from ..types import Balance, balance_list_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import maybe_transform
from .._resource import SyncAPIResource, AsyncAPIResource
from ..pagination import SyncSinglePage, AsyncSinglePage
from .._base_client import AsyncPaginator, make_request_options

__all__ = ["Balances", "AsyncBalances"]


class Balances(SyncAPIResource):
    def list(
        self,
        *,
        account_token: str | NotGiven = NOT_GIVEN,
        balance_date: Union[str, datetime] | NotGiven = NOT_GIVEN,
        financial_account_type: Literal["ISSUING", "RESERVE"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
    ) -> SyncSinglePage[Balance]:
        """
        Get the balances for a program or a given end-user account

        Args:
          account_token: List balances for all financial accounts of a given account_token.

          balance_date: UTC date and time of the balances to retrieve. Defaults to latest available
              balances

          financial_account_type: List balances for a given Financial Account type.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/balances",
            page=SyncSinglePage[Balance],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_token": account_token,
                        "balance_date": balance_date,
                        "financial_account_type": financial_account_type,
                    },
                    balance_list_params.BalanceListParams,
                ),
            ),
            model=Balance,
        )


class AsyncBalances(AsyncAPIResource):
    def list(
        self,
        *,
        account_token: str | NotGiven = NOT_GIVEN,
        balance_date: Union[str, datetime] | NotGiven = NOT_GIVEN,
        financial_account_type: Literal["ISSUING", "RESERVE"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[Balance, AsyncSinglePage[Balance]]:
        """
        Get the balances for a program or a given end-user account

        Args:
          account_token: List balances for all financial accounts of a given account_token.

          balance_date: UTC date and time of the balances to retrieve. Defaults to latest available
              balances

          financial_account_type: List balances for a given Financial Account type.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/balances",
            page=AsyncSinglePage[Balance],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_token": account_token,
                        "balance_date": balance_date,
                        "financial_account_type": financial_account_type,
                    },
                    balance_list_params.BalanceListParams,
                ),
            ),
            model=Balance,
        )
