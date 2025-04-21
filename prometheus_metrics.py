from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily
import decoder


def get_attribute(data, meter, cluster, attribute):
    '''Gets a value from the data structure'''
    if meter in data:
        if cluster in data[meter]:
            if attribute in data[meter][cluster]:
                return data[meter][cluster][attribute]
    return None


def value_modifier_div_1000(output, data, value):
    return value/1000


def bill_to_date_conversion(output, data, value):
    trailing_digits_attribute = get_attribute(
        data,
        output["meter"],
        decoder.Cluster.metering.value,
        decoder.MeteringParmeter.bill_delivered_trailing_digit.value)
    trailing_digits = trailing_digits_attribute["value"] >> 4

    return value / pow(10, trailing_digits)


def prepayment_currency_converion(output, data, value):
    # this value is stored in another register however this is not read by the device
    return value / pow(10, 5)


output_fields = [
    # electric
    {
        "meter": b'\x99\x57',
        "cluster": decoder.Cluster.metering.value,
        "attribute": decoder.MeteringParmeter.instantaneous_demand.value,
        "metric_type": GaugeMetricFamily,
        "metric_name": "smart_meter_electric_metering_instantaneous_demand_watts",
        "metric_description": "instentaneous power reported by the smart meter in watts"
    },
    {
        "meter": b'\x99\x57',
        "cluster": decoder.Cluster.metering.value,
        "attribute": decoder.MeteringParmeter.current_summation_delivered.value,
        "metric_type": CounterMetricFamily,
        "metric_name": "smart_meter_electric_metering_current_summation_delivered_watthours",
        "metric_description": "current meter reading in watt hours",
    },
    {
        "meter": b'\x99\x57',
        "cluster": decoder.Cluster.metering.value,
        "attribute": decoder.MeteringParmeter.current_summation_received.value,
        "metric_type": CounterMetricFamily,
        "metric_name": "smart_meter_electric_metering_current_summation_recieved_watthours",
        "metric_description": "current export meter reading in watt hours",
    },
    {
        "meter": b'\x99\x57',
        "cluster": decoder.Cluster.metering.value,
        "attribute": decoder.MeteringParmeter.bill_to_date_delivered.value,
        "metric_type": GaugeMetricFamily,
        "attribute_modifier": bill_to_date_conversion,
        "metric_name": "smart_meter_electric_metering_bill_to_date_delivered",
        "metric_description": "total cost in current billing cycle",
    },
    {
        "meter": b'\x99\x57',
        "cluster": decoder.Cluster.metering.value,
        "attribute": decoder.MeteringParmeter.current_day_consumption_delivered.value,
        "metric_type": GaugeMetricFamily,
        "metric_name": "smart_meter_electric_metering_current_day_consumption_delivered_watthours",
        "metric_description": "amount of energy consumed today",
    },
    {
        "meter": b'\x99\x57',
        "cluster": decoder.Cluster.metering.value,
        "attribute": decoder.MeteringParmeter.previous_day_consumption_delivered.value,
        "metric_type": GaugeMetricFamily,
        "metric_name": "smart_meter_electric_metering_previous_day_consumption_delivered_watthours",
        "metric_description": "amount of energy consumed yesterday",
    },
    {
        "meter": b'\x99\x57',
        "cluster": decoder.Cluster.metering.value,
        "attribute": decoder.MeteringParmeter.current_week_consumption_delivered.value,
        "metric_type": GaugeMetricFamily,
        "metric_name": "smart_meter_electric_metering_current_week_consumption_delivered_watthours",
        "metric_description": "amount of energy consumed this week",
    },
    {
        "meter": b'\x99\x57',
        "cluster": decoder.Cluster.metering.value,
        "attribute": decoder.MeteringParmeter.previous_week_consumption_delivered.value,
        "metric_type": GaugeMetricFamily,
        "metric_name": "smart_meter_electric_metering_previous_week_consumption_delivered_watthours",
        "metric_description": "amount of energy consumed last week",
    },
    {
        "meter": b'\x99\x57',
        "cluster": decoder.Cluster.metering.value,
        "attribute": decoder.MeteringParmeter.current_month_consumption_delivered.value,
        "metric_type": GaugeMetricFamily,
        "metric_name": "smart_meter_electric_metering_current_month_consumption_delivered_watthours",
        "metric_description": "amount of energy consumed this month",
    },
    {
        "meter": b'\x99\x57',
        "cluster": decoder.Cluster.metering.value,
        "attribute": decoder.MeteringParmeter.previous_month_consumption_delivered.value,
        "metric_type": GaugeMetricFamily,
        "metric_name": "smart_meter_electric_metering_previous_month_consumption_delivered_watthours",
        "metric_description": "amount of energy consumed last month",
    },
    {
        "meter": b'\x99\x57',
        "cluster": decoder.Cluster.prepayment.value,
        "attribute": decoder.PrepaymentParameter.current_day_cost_consumption_delivered.value,
        "attribute_modifier": prepayment_currency_converion,
        "metric_type": GaugeMetricFamily,
        "metric_name": "smart_meter_electric_prepayment_current_day_cost_consumption_delivered",
        "metric_description": "cost of energy consumed today",
    },
    {
        "meter": b'\x99\x57',
        "cluster": decoder.Cluster.prepayment.value,
        "attribute": decoder.PrepaymentParameter.previous_day_cost_consumption_delivered.value,
        "attribute_modifier": prepayment_currency_converion,
        "metric_type": GaugeMetricFamily,
        "metric_name": "smart_meter_electric_prepayment_previous_day_cost_consumption_delivered",
        "metric_description": "cost of energy consumed yesterday",
    },
    {
        "meter": b'\x99\x57',
        "cluster": decoder.Cluster.prepayment.value,
        "attribute": decoder.PrepaymentParameter.current_week_cost_consumption_delivered.value,
        "attribute_modifier": prepayment_currency_converion,
        "metric_type": GaugeMetricFamily,
        "metric_name": "smart_meter_electric_prepayment_current_week_cost_consumption_delivered",
        "metric_description": "cost of energy consumed this week",
    },
    {
        "meter": b'\x99\x57',
        "cluster": decoder.Cluster.prepayment.value,
        "attribute": decoder.PrepaymentParameter.previous_week_cost_consumption_delivered.value,
        "attribute_modifier": prepayment_currency_converion,
        "metric_type": GaugeMetricFamily,
        "metric_name": "smart_meter_electric_prepayment_previous_week_cost_consumption_delivered",
        "metric_description": "cost of energy consumed last week",
    },
    {
        "meter": b'\x99\x57',
        "cluster": decoder.Cluster.prepayment.value,
        "attribute": decoder.PrepaymentParameter.current_month_cost_consumption_delivered.value,
        "attribute_modifier": prepayment_currency_converion,
        "metric_type": GaugeMetricFamily,
        "metric_name": "smart_meter_electric_prepayment_current_month_cost_consumption_delivered",
        "metric_description": "cost of energy consumed this month",
    },
    {
        "meter": b'\x99\x57',
        "cluster": decoder.Cluster.prepayment.value,
        "attribute": decoder.PrepaymentParameter.previous_month_cost_consumption_delivered.value,
        "attribute_modifier": prepayment_currency_converion,
        "metric_type": GaugeMetricFamily,
        "metric_name": "smart_meter_electric_prepayment_previous_month_cost_consumption_delivered",
        "metric_description": "cost of energy consumed last month",
    },

    # gas
    {
        "meter": b'\x00\x00',
        "cluster": decoder.Cluster.metering.value,
        "attribute": decoder.MeteringParmeter.current_summation_delivered.value,
        "attribute_modifier": value_modifier_div_1000,
        "metric_type": CounterMetricFamily,
        "metric_name": "smart_meter_gas_metering_current_summation_delivered_m3",
        "metric_description": "current meter reading in cubic meters",
    },
    {
        "meter": b'\x00\x00',
        "cluster": decoder.Cluster.metering.value,
        "attribute": decoder.MeteringParmeter.bill_to_date_delivered.value,
        "metric_type": GaugeMetricFamily,
        "attribute_modifier": bill_to_date_conversion,
        "metric_name": "smart_meter_gas_metering_bill_to_date_delivered",
        "metric_description": "total cost in current billing cycle",
    },
    {
        "meter": b'\x00\x00',
        "cluster": decoder.Cluster.metering.value,
        "attribute": decoder.MeteringParmeter.current_day_alternative_consumption_delivered.value,
        "metric_type": GaugeMetricFamily,
        "metric_name": "smart_meter_gas_metering_current_day_alternative_consumption_delivered_watthours",
        "metric_description": "amount of gas consumed today",
    },
    {
        "meter": b'\x00\x00',
        "cluster": decoder.Cluster.metering.value,
        "attribute": decoder.MeteringParmeter.previous_day_alternative_consumption_delivered.value,
        "metric_type": GaugeMetricFamily,
        "metric_name": "smart_meter_gas_metering_previous_day_alternative_consumption_delivered_watthours",
        "metric_description": "amount of gas consumed yesterday",
    },
    {
        "meter": b'\x00\x00',
        "cluster": decoder.Cluster.metering.value,
        "attribute": decoder.MeteringParmeter.current_week_alternative_consumption_delivered.value,
        "metric_type": GaugeMetricFamily,
        "metric_name": "smart_meter_gas_metering_current_week_alternative_consumption_delivered_watthours",
        "metric_description": "amount of gas consumed this week",
    },
    {
        "meter": b'\x00\x00',
        "cluster": decoder.Cluster.metering.value,
        "attribute": decoder.MeteringParmeter.previous_week_alternative_consumption_delivered.value,
        "metric_type": GaugeMetricFamily,
        "metric_name": "smart_meter_gas_metering_previous_week_alternative_consumption_delivered_watthours",
        "metric_description": "amount of gas consumed last week",
    },
    {
        "meter": b'\x00\x00',
        "cluster": decoder.Cluster.metering.value,
        "attribute": decoder.MeteringParmeter.current_month_alternative_consumption_delivered.value,
        "metric_type": GaugeMetricFamily,
        "metric_name": "smart_meter_gas_metering_current_month_alternative_consumption_delivered_watthours",
        "metric_description": "amount of gas consumed this month",
    },
    {
        "meter": b'\x00\x00',
        "cluster": decoder.Cluster.metering.value,
        "attribute": decoder.MeteringParmeter.previous_month_alternative_consumption_delivered.value,
        "metric_type": GaugeMetricFamily,
        "metric_name": "smart_meter_gas_metering_previous_month_alternative_consumption_delivered_watthours",
        "metric_description": "amount of gas consumed last month",
    },
    {
        "meter": b'\x00\x00',
        "cluster": decoder.Cluster.prepayment.value,
        "attribute": decoder.PrepaymentParameter.current_day_cost_consumption_delivered.value,
        "attribute_modifier": prepayment_currency_converion,
        "metric_type": GaugeMetricFamily,
        "metric_name": "smart_meter_gas_prepayment_current_day_cost_consumption_delivered",
        "metric_description": "cost of energy consumed today",
    },
    {
        "meter": b'\x00\x00',
        "cluster": decoder.Cluster.prepayment.value,
        "attribute": decoder.PrepaymentParameter.previous_day_cost_consumption_delivered.value,
        "attribute_modifier": prepayment_currency_converion,
        "metric_type": GaugeMetricFamily,
        "metric_name": "smart_meter_gas_prepayment_previous_day_cost_consumption_delivered",
        "metric_description": "cost of energy consumed yesterday",
    },
    {
        "meter": b'\x00\x00',
        "cluster": decoder.Cluster.prepayment.value,
        "attribute": decoder.PrepaymentParameter.current_week_cost_consumption_delivered.value,
        "attribute_modifier": prepayment_currency_converion,
        "metric_type": GaugeMetricFamily,
        "metric_name": "smart_meter_gas_prepayment_current_week_cost_consumption_delivered",
        "metric_description": "cost of energy consumed this week",
    },
    {
        "meter": b'\x00\x00',
        "cluster": decoder.Cluster.prepayment.value,
        "attribute": decoder.PrepaymentParameter.previous_week_cost_consumption_delivered.value,
        "attribute_modifier": prepayment_currency_converion,
        "metric_type": GaugeMetricFamily,
        "metric_name": "smart_meter_gas_prepayment_previous_week_cost_consumption_delivered",
        "metric_description": "cost of energy consumed last week",
    },
    {
        "meter": b'\x00\x00',
        "cluster": decoder.Cluster.prepayment.value,
        "attribute": decoder.PrepaymentParameter.current_month_cost_consumption_delivered.value,
        "attribute_modifier": prepayment_currency_converion,
        "metric_type": GaugeMetricFamily,
        "metric_name": "smart_meter_gas_prepayment_current_month_cost_consumption_delivered",
        "metric_description": "cost of energy consumed this month",
    },
    {
        "meter": b'\x00\x00',
        "cluster": decoder.Cluster.prepayment.value,
        "attribute": decoder.PrepaymentParameter.previous_month_cost_consumption_delivered.value,
        "attribute_modifier": prepayment_currency_converion,
        "metric_type": GaugeMetricFamily,
        "metric_name": "smart_meter_gas_prepayment_previous_month_cost_consumption_delivered",
        "metric_description": "cost of energy consumed last month",
    },
    ]
