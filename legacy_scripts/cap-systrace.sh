#!/bin/sh

workload()
{

}

setDrmTracingMark()
{
	adb shell "echo $1 > /sys/kernel/debug/tracing/events/drm/tracing_mark_write/enable"
}

setTracing()
{

	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_flip_request/enable"
	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_flip_complete/enable"

	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_gem_evict/enable"
	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_gem_evict_everything/enable"
	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_gem_evict_vm/enable"

	#adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_gem_object_change_domain/enable"
	#adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_gem_object_clflush/enable"
	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_gem_object_create/enable"
	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_gem_object_destroy/enable"
	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_gem_object_fault/enable"
	#adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_gem_object_pread/enable"
	#adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_gem_object_pwrite/enable"

	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_gem_request_add/enable"
	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_gem_request_complete/enable"
	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_gem_request_notify/enable"
	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_gem_request_retire/enable"
	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_gem_request_wait_begin/enable"
	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_gem_request_wait_end/enable"

	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_gem_ring_dispatch/enable"
	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_gem_ring_flush/enable"
	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_gem_ring_queue/enable"
	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_gem_ring_sync_to/enable"


	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_ring_wait_begin/enable"
	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_ring_wait_end/enable"

	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_scheduler_destroy/enable"
	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_scheduler_fly/enable"
	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_scheduler_irq/enable"
	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_scheduler_landing/enable"
	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_scheduler_node_state_change/enable"
	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_scheduler_pop_from_queue/enable"
	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_scheduler_queue/enable"
	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_scheduler_remove/enable"
	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/i915_scheduler_unfly/enable"

	adb shell "echo $1 > /sys/kernel/debug/tracing/events/i915/intel_gpu_freq_change/enable"
}

main()
{
	if [ $# -ne 1 ]
	then
		echo "Error: Require trace file path"
		return
	fi

	setTracing 1
	setDrmTracingMark 1

	workload

	python systrace.py --time=10 -b 60000 sched gfx video -o $1

	setDrmTracingMark 0
	setTracing 0
}

main "$@"

