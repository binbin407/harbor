// Copyright Project Harbor Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//    http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package flow

import (
	"testing"

	"github.com/goharbor/harbor/src/replication/ng/model"
	"github.com/stretchr/testify/require"
)

func TestRunOfDeletionFlow(t *testing.T) {
	scheduler := &fakedScheduler{}
	executionMgr := &fakedExecutionManager{}
	registryMgr := &fakedRegistryManager{}
	policy := &model.Policy{}
	resources := []*model.Resource{}
	flow := NewDeletionFlow(executionMgr, registryMgr, scheduler, 1, policy, resources)
	err := flow.Run(nil)
	require.Nil(t, err)
}