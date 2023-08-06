#pragma once

#include <tuple>

#include "../config.h"
#include "../macros.h"

namespace inference::quantization::params {

class QuantParams {
   private:
    int64_t bins, upsample_rate;

   public:
    using State = std::tuple<int64_t, int64_t>;

    QuantParams(const config::Config &config)
        : bins(config.default_histogram_bins), upsample_rate(config.default_histogram_upsample_rate) {}
    QuantParams(QuantParams::State state) : bins(std::get<0>(state)), upsample_rate(std::get<1>(state)) {}

    /* Bins accessors */
    int64_t get_bins() { return bins; }
    void set_bins(int64_t val) { bins = val; }

    /* Upsample rate accessors */
    int64_t get_upsample_rate() { return upsample_rate; }
    void set_upsample_rate(int64_t val) { upsample_rate = val; }

    /* Serialization */
    State serialize();
    static QuantParams deserialize(const QuantParams::State &state);
};

class Params {
   private:
    bool fake_quantize_enabled, observer_enabled, track_quant_stats;
    std::shared_ptr<QuantParams> quant;

   public:
    using State = std::tuple<bool, bool, bool, QuantParams::State>;

    Params(const config::Config &config)
        : fake_quantize_enabled(config.default_fake_quantize_enabled),
          observer_enabled(config.default_observer_enabled),
          track_quant_stats(config.default_track_quant_stats),
          quant(std::make_shared<QuantParams>(config)) {}
    Params(Params::State state)
        : fake_quantize_enabled(std::get<0>(state)),
          observer_enabled(std::get<1>(state)),
          track_quant_stats(std::get<2>(state)),
          quant(std::make_shared<QuantParams>(std::get<3>(state))) {}
    Params(const Params &other)
        : fake_quantize_enabled(other.fake_quantize_enabled),
          observer_enabled(other.observer_enabled),
          track_quant_stats(other.track_quant_stats),
          quant(other.quant) {}

    /* Accessors for fake quantize option. */
    void set_fake_quantize_enabled(bool val) { fake_quantize_enabled = val; }
    bool get_fake_quantize_enabled() { return fake_quantize_enabled; }

    /* Accessors for observer option. */
    void set_observer_enabled(bool val) { observer_enabled = val; }
    bool get_observer_enabled() { return observer_enabled; }

    /* Accessors for histogram bins. */
    std::shared_ptr<QuantParams> &get_quant_params() { return quant; }

    /* Accessors for quant stats option. */
    void set_track_quant_stats(bool val) { track_quant_stats = val; }
    bool get_track_quant_stats() { return track_quant_stats; }

    /* Serialization */
    State serialize();
    static Params deserialize(const Params::State &state);
};

}  // namespace inference::quantization::params
