from dataclasses import dataclass
from typing import *
@dataclass
class PreferredFrequencyDetails:
    preferredCarrier0Freq: "FrequencyRange"
    preferredCarrier1Freq: "FrequencyRange"

    @staticmethod
    def from_dict(obj) -> "PreferredFrequencyDetails":
        _preferredCarrier0Freq = FrequencyRange.from_dict(obj.get("preferredCarrier0Freq"))
        _preferredCarrier1Freq = FrequencyRange.from_dict(obj.get("preferredCarrier1Freq"))
        return PreferredFrequencyDetails(_preferredCarrier0Freq, _preferredCarrier1Freq)


@dataclass
class FrequencyRange:
    lowerFreqKhz: int
    upperFreqKhz: int

    def __contains__(self, freq_range: "FrequencyRange"):
        return freq_range.lowerFreqKhz >= self.lowerFreqKhz and freq_range.upperFreqKhz <= self.upperFreqKhz

    def __eq__(self, obj: object) -> bool:
        return (
            isinstance(obj, FrequencyRange)
            and obj.lowerFreqKhz == self.lowerFreqKhz
            and obj.upperFreqKhz == self.upperFreqKhz
        )

    @staticmethod
    def from_dict(obj: Any) -> "FrequencyRange":
        _lowerFreqKhz = obj.get("lowerFreqKhz")
        _upperFreqKhz = obj.get("upperFreqKhz")
        return FrequencyRange(_lowerFreqKhz, _upperFreqKhz)


type_hints = get_type_hints(PreferredFrequencyDetails)

print(type_hints)

from datatable_faker import generate_fake_data

l=generate_fake_data(PreferredFrequencyDetails)

print(l)